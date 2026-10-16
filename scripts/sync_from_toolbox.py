"""sync_from_toolbox.py - copy my showcased work from the Toolbox repo into this portfolio.

Toolbox (github.com/netnovaops-training/Toolbox) is where I work and take notes. This
repo is the clean version for anyone reviewing my work. An entry is copied here when it
is finished and worth showing: a resolved project, or anything with `showcase: true`.

Writes:
  work/<entry>.md   a clean copy of each showcased write-up
  work/README.md    the list of them
  LESSONS.md        the lessons from that work, grouped by technology
  README.md         only the part between the LATEST WORK markers

Usage:  python -I scripts/sync_from_toolbox.py <path-to-a-Toolbox-checkout>
No third-party packages. Same input -> same output (safe to run any time).
"""
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLBOX_URL = "https://github.com/netnovaops-training/Toolbox"
BEGIN, END = "<!-- BEGIN LATEST WORK -->", "<!-- END LATEST WORK -->"
GENERATED = "<!-- GENERATED from the Toolbox repo by scripts/sync_from_toolbox.py - do not edit by hand. -->"
LATEST_LIMIT = 5


def load_toolbox(path):
    spec = importlib.util.spec_from_file_location("build_index", path / "code/local/build_index.py")
    bi = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bi)  # its ROOT is the Toolbox checkout, so load_entries() reads it
    return bi


def clean_body(text):
    """Drop the frontmatter, instruction comments and the first heading."""
    text = text.replace("\r\n", "\n")
    if text.startswith("---\n"):
        text = text[text.find("\n---\n", 3) + 5:]
    text = re.sub(r"<!--.*?-->\n?", "", text, flags=re.S)
    text = re.sub(r"\A\s*# [^\n]*\n", "", text)
    return text.strip() + "\n"


def title_of(e):
    t = e["title"]
    return t[:1].upper() + t[1:]


def render_entry(bi, e, toolbox):
    body = clean_body((toolbox / e["path"]).read_text(encoding="utf-8"))
    tags = " ".join(f"`{t}`" for t in e["tech"])
    head = [
        f"# {title_of(e)}",
        "",
        GENERATED,
        "",
        f"**{bi.TYPE_NAME.get(e['type'], e['type'])}** · finished {e.get('closed') or e['date']}"
        + (f" · {tags}" if tags else ""),
        "",
        f"> {e['summary']}",
        "",
    ]
    tail = [
        "",
        "---",
        "",
        f"**Takeaway:** {e['lesson']}",
        "",
        f"[Original notes in my Toolbox]({TOOLBOX_URL}/blob/main/{e['path']})",
        "",
    ]
    return "\n".join(head) + "\n" + body + "\n".join(tail)


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"wrote: {path.relative_to(ROOT).as_posix()}")
    return True


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    toolbox = Path(argv[0]).resolve()
    bi = load_toolbox(toolbox)
    entries, errors = bi.load_entries()
    if errors:
        print("Toolbox has entries with problems (skipped):", *errors, sep="\n  ")
    shown = [e for e in entries if bi.showcased(e)]

    work = ROOT / "work"
    keep = {"README.md"}
    for e in shown:
        name = Path(e["path"]).name
        keep.add(name)
        write(work / name, render_entry(bi, e, toolbox))
    for old in work.glob("*.md") if work.exists() else []:
        if old.name not in keep:
            old.unlink()
            print(f"removed: work/{old.name}")

    # work/README.md - the list
    lines = ["# Work", "", GENERATED, "",
             "Finished pieces of work, each with what I did, what went wrong and what I learned.", ""]
    if shown:
        lines += ["| Finished | Work | Type | Tools |", "|---|---|---|---|"]
        for e in shown:
            lines.append(f"| {e.get('closed') or e['date']} | [{bi.cell(title_of(e))}]({Path(e['path']).name}) "
                         f"| {bi.TYPE_NAME.get(e['type'], e['type'])} | {bi.tech_text(e)} |")
    else:
        lines.append("_Finished work appears here automatically._")
    write(work / "README.md", "\n".join(lines) + "\n")

    # LESSONS.md - grouped by technology
    techs = sorted({t for e in shown for t in e["tech"]})
    out = ["# Lessons learned", "", GENERATED, "",
           "What each piece of finished work taught me, grouped by technology.", ""]
    if not shown:
        out.append("_Lessons appear here as work is finished._")
    for t in techs:
        out += [f"## {t}", ""]
        for e in shown:
            if t in e["tech"]:
                out.append(f"- {bi.cell(e['lesson'])} - [{bi.cell(title_of(e))}](work/{Path(e['path']).name})")
        out.append("")
    write(ROOT / "LESSONS.md", "\n".join(out).rstrip() + "\n")

    # README.md - only between the markers
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    if BEGIN in text and END in text:
        latest = []
        for e in shown[:LATEST_LIMIT]:
            tags = " ".join(f"`{t}`" for t in e["tech"])
            latest.append(f"- **[{bi.cell(title_of(e))}](work/{Path(e['path']).name})** - "
                          f"{bi.cell(e['summary'])}" + (f"  \n  {tags}" if tags else ""))
        if shown:
            latest.append("\n[All finished work](work/) · [Lessons learned](LESSONS.md)")
        else:
            latest.append("_My newest finished work appears here automatically._")
        head, rest = text.split(BEGIN, 1)
        _, tail = rest.split(END, 1)
        write(readme, f"{head}{BEGIN}\n" + "\n".join(latest) + f"\n{END}{tail}")
    print(f"{len(shown)} showcased entries")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
