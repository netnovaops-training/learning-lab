# Portfolio

Real work on a self-hosted web app and its release and security pipeline. Each
item has a plain summary and a short engineering note. The public proof is the
repository **[netnovaops-training/garden-for-all](https://github.com/netnovaops-training/garden-for-all)**.

---

## Verified, tamper-evident software delivery

**Plain:** The app's installer downloads the program from the internet and
checks every single file against a published list of fingerprints before it uses
any of it. If one file is wrong, missing or extra, it writes nothing and says so.

**Engineering note:** A slim data package carries only the owner's own data; on
first run the installer fetches the code from a public Git host and verifies each
file's SHA-256 against a tracked `CODE-FINGERPRINTS.txt`, failing closed on any
mismatch. A pinned commit can be named instead of a branch to stay on a fixed,
checked version. This gives a small download, fast updates, and integrity that
does not depend on trusting the transport.

## Resilient multi-source downloads

**Plain:** A large file is split into small pieces, each with its own
fingerprint, and the pieces are pulled from several places at once. If one place
is slow or down, the others cover it. Nothing is downloaded twice.

**Engineering note:** The 800 MB asset is split into ~25 MB parts with a JSON
manifest (name, size, SHA-256, per-part host list). A work-queue downloader runs
one connection per host, claims the next unclaimed part, resumes cut-off parts
with HTTP Range, drops a host after repeated failures, and re-fetches only a bad
part. A "pinned" first part is fetched first and preferred from one host, with a
private-repo fallback.

## Encrypting private data in a public distribution

**Plain:** Private files travel inside the public download, but encrypted, so
only someone with the key can open them. The key is delivered separately.

**Engineering note:** AES-256 (openssl, streamed) with the key shipped only in
the owner's private data package; integrity by per-part SHA-256 checked before
decryption and a whole-file hash after. A short-lived read-only token for the
fallback host is removed from disk once the full set is installed.

## CI/CD security pipeline (GitHub Actions)

**Plain:** Every change is automatically checked for bugs, security holes,
secrets and out-of-date libraries. Deep scans run on a schedule and more often
during heavy coding.

**Engineering note:** Workflows for CodeQL, Semgrep, Trivy, OSV-Scanner, Bandit,
cargo-audit, pip-audit, ShellCheck, PSScriptAnalyzer, Clippy, detekt, Dependency
Review and OpenSSF Scorecard. Every third-party action pinned to a commit SHA,
least-privilege `permissions:` per job, concurrency cancellation, path filters,
and a "burst gate" that runs the expensive scans only when recent commit
activity is high. SARIF uploads are tuned so only the rarely-wrong findings raise
alerts and noise stays in artifacts.

## Supply-chain integrity automation

**Plain:** A small bot keeps the fingerprint list correct automatically, so a
routine change can never quietly break the verified download.

**Engineering note:** A workflow regenerates and commits `CODE-FINGERPRINTS.txt`
on pushes, and a required `fingerprints-in-sync` check fails a pull request whose
list does not match the tree. This closed a real failure mode found when a
dependency-update merge left the list stale.

## Vulnerability triage and remediation

**Plain:** Reviewed every security alert, fixed the real ones with tests, and
dismissed the false ones with a written reason, then confirmed with a clean
install from scratch.

**Engineering note:** Triaged 17 CodeQL alerts (path-injection, DOM-XSS,
SSRF, clear-text, hard-coded value): rewrote a path check into a form the
analyser recognises (normalise, confirm prefix, re-check the real path,
extension allowlist), replaced an inline-script sink with a data attribute and
listener, added HTML escaping, and dismissed the false positives with reasons.
Verified by a fresh end-to-end install that reported all files matched.

## Safe release flow

**Plain:** The released line is protected. New work happens on side branches and
only reaches the release after review and passing checks.

**Engineering note:** `main` is the released branch that installs follow;
`fixes` and `enhancements` stage changes; merges go through pull requests with
Copilot review and required checks; Dependabot targets the staging branch, not
the release.

---

## Skills shown here

Linux and Windows administration · Docker and Docker Compose · Rust, Python,
Kotlin, shell, PowerShell · Git and GitHub (branches, pull requests, Actions) ·
DevSecOps (SAST, SCA, secret scanning, supply-chain integrity) · cryptography
and key handling · troubleshooting and root-cause fixes · clear documentation in
plain language.
