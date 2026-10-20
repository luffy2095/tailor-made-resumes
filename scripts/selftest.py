#!/usr/bin/env python3
"""Contributor self-test. Builds every example in a temporary copy and checks the build's guards.

    python3 -u scripts/selftest.py            # about 1 min, needs scripts/setup.py to have passed
    python3 -u scripts/selftest.py --links    # also checks every \\href URL returns 200 (network)

Exit 0 only when every check passes. Nothing in the repo is modified.
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = [sys.executable, os.path.join(ROOT, "scripts", "build.py")]
EXPECTED_PAGES = {"cheatsheet": 2, "cheatsheet_ledgers": 2}   # every other example is a 1-page resume
failures = []


def check(name, ok, detail=""):
    print(f"  {'ok  ' if ok else 'FAIL'} {name}{'  ' + detail if detail and not ok else ''}", flush=True)
    if not ok:
        failures.append(name)


def build(path, *extra):
    return subprocess.run([*BUILD, path, *extra], capture_output=True, text=True)


def main():
    links = "--links" in sys.argv
    with tempfile.TemporaryDirectory() as tmp:
        print("## 1. Examples build to their page counts", flush=True)
        shutil.copytree(os.path.join(ROOT, "examples"), os.path.join(tmp, "examples"))
        for tex in sorted(glob.glob(os.path.join(tmp, "examples", "**", "*.tex"), recursive=True)):
            name = os.path.basename(tex)[:-4]
            pages = EXPECTED_PAGES.get(name, 1)
            r = build(tex, "--pages", str(pages))
            check(f"{os.path.relpath(tex, tmp)} ({pages} p)", r.returncode == 0, (r.stdout + r.stderr).strip()[-300:])

        print("## 2. Templates: refused while unfilled, compile for previews", flush=True)
        os.makedirs(os.path.join(tmp, "templates"))
        for src in sorted(glob.glob(os.path.join(ROOT, "templates", "*.tex"))):
            tex = os.path.join(tmp, "templates", os.path.basename(src))
            shutil.copy(src, tex)
            check(f"{os.path.basename(src)} refused unfilled", build(tex).returncode == 1)
            r = build(tex, "--allow-placeholders")
            check(f"{os.path.basename(src)} compiles", r.returncode == 0, (r.stdout + r.stderr).strip()[-300:])

        print("## 3. ATS guard catches ligatures", flush=True)
        ats = os.path.join(tmp, "examples", "ria-kapoor", "jobs", "ledgerline-senior-backend-payments", "ats.tex")
        src = open(ats).read()   # read before opening for write: "w" truncates the file
        open(ats, "w").write(re.sub(r".*DisableLigatures.*\n", "", src))
        r = build(ats, "--pages", "1")
        if shutil.which("pdftotext"):
            check("ligatures re-enabled -> build fails", r.returncode == 4, r.stdout[-200:])
        else:
            print("  skip (no pdftotext)")

    if links:
        print("## 4. Every link resolves", flush=True)
        urls = set()
        for f in glob.glob(os.path.join(ROOT, "**", "*.tex"), recursive=True):
            urls |= {u for u in re.findall(r"\\href\{(https?://[^}]+)\}", open(f).read()) if "PH-" not in u and "example.com" not in u}
        for u in sorted(urls):
            try:
                code = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=20).status
            except Exception as e:
                code = getattr(e, "code", type(e).__name__)
            check(u, code == 200, str(code))

    print(f"\n{'all checks passed' if not failures else f'{len(failures)} check(s) failed'}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
