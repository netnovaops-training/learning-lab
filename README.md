# Jason A. Gibson

**Working toward an infrastructure / systems engineering role.**
I build and run my own systems, break them on purpose, fix them, and write down what I learned.

CompTIA **Security+** · Studying for Network+ / CCNA and Linux+

---

## Projects

### Jun's Garden — self-hosted website, packaged for someone else to run
[Case study](case-studies/juns-garden.md) · [Code](https://github.com/netnovaops-training/garden-for-all)

A complete garden website (plant catalogue, blog, garden tools, Android app) that I
moved from PHP to Rust and then handed over to its owner to run on his own computer.

- Rebuilt the site in **Rust** page by page, keeping every page, address and feature the same.
- Wrote **guided installers** for Ubuntu and Windows that explain each step, plus guides in English and Korean.
- Each program runs in its own **Docker** container; only the front door faces the internet.
- Installs check every file against a published fingerprint list and **stop if anything doesn't match**.
- Set up **security scanning** on every change (CodeQL, Semgrep, Trivy, dependency updates) and worked through every finding.

`Rust` `Docker` `Linux` `PowerShell` `Python` `Kotlin` `GitHub Actions` `Security`

### Toolbox — my working notes, run like a ticket system
[Code](https://github.com/netnovaops-training/Toolbox)

- Every fix, install and project is a **ticket** with a write-up, worked on a branch and merged into `main` through a pull request.
- Scripts I built **sort everything automatically** by topic, language and branch, and finished work is copied here by itself.
- A step-by-step **learning path** for networking, Linux, security and git, with runnable examples.

`Git` `GitHub Actions` `Bash` `Python` `Markdown`

---

## Latest work

<!-- BEGIN LATEST WORK -->
_My newest finished work appears here automatically._
<!-- END LATEST WORK -->

## Skills

| Area | Where to see it |
|---|---|
| **Networking** | [ssh, curl, dig](https://github.com/netnovaops-training/Toolbox/tree/main/learn/01-network-connect) · [tcpdump, nmap](https://github.com/netnovaops-training/Toolbox/tree/main/learn/02-network-capture-and-scan) |
| **Linux** | [shell and files](https://github.com/netnovaops-training/Toolbox/tree/main/learn/03-shell-and-files) · [system and performance](https://github.com/netnovaops-training/Toolbox/tree/main/learn/05-system-and-performance) |
| **Containers** | [Jun's Garden](case-studies/juns-garden.md) · [fixing a volume permission error](https://github.com/netnovaops-training/Toolbox/blob/main/knowledge/troubleshooting/2026-10-15-container-volume-permission-denied.md) |
| **Security** | Security+ · [delivery and CI security in Jun's Garden](case-studies/juns-garden.md) |
| **Automation** | [GitHub Actions in Toolbox](https://github.com/netnovaops-training/Toolbox/tree/main/.github/workflows) · [this repo's sync job](.github/workflows/sync-from-toolbox.yml) |
| **Git** | [branch and pull request workflow](https://github.com/netnovaops-training/Toolbox/blob/main/knowledge/projects/2026-10-15-add-branches-to-flow.md) |

---

_This page updates itself: finished work from my [Toolbox](https://github.com/netnovaops-training/Toolbox)
is copied in every day. [All finished work](work/) · [Lessons learned](LESSONS.md)_
