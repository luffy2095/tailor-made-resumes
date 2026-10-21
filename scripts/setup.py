#!/usr/bin/env python3
"""One-time setup: install TinyTeX if missing, add the packages the templates use, compile a smoke page.

    python3 -u setup.py > setup.log 2>&1      # 2-6 min on a fresh machine, mostly download

Prints a line before each phase so a slow download is never silent. Exit 0 = LaTeX ready.
"""
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tex  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):   # Windows pipes default to cp1252; ligature words would crash print
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PACKAGES = ["carlito", "opensans", "xcharter", "enumitem", "titlesec", "xcolor", "hyperref", "geometry",
            "pgf", "paracol", "ragged2e", "fontawesome5", "eso-pic", "xstring", "carlisle", "microtype", "latexmk",
            # fallback and typewriter fonts: a fresh TinyTeX lacks them, and \texttt or a TS1 symbol needs them
            "fontaxes", "ec", "cm-super", "lm"]
INSTALL_UNIX = "https://tinytex.yihui.org/install-bin-unix.sh"
# The official .bat wrapper passes its URL to curl in single quotes, which cmd keeps literally (broken as of 2026-10).
# Run the PowerShell installer it wraps instead.
INSTALL_WIN = "https://tinytex.yihui.org/install-bin-windows.ps1"
T0 = time.time()

SMOKE = r"""
\documentclass[10pt,a4paper]{article}
\usepackage[T1]{fontenc}\usepackage{carlito}\usepackage{opensans}\usepackage{XCharter}
\usepackage[margin=0.6in]{geometry}\usepackage{enumitem}\usepackage{titlesec}\usepackage{xcolor}
\usepackage{tikz}\usepackage{paracol}\usepackage{ragged2e}\usepackage{fontawesome5}\usepackage{eso-pic}
\usepackage[hidelinks]{hyperref}
\begin{document}
\section*{Smoke test}
{\fontfamily{Carlito-TLF}\selectfont Carlito} {\fontfamily{opensans-TLF}\selectfont Open Sans} {\fontfamily{XCharter-TLF}\selectfont XCharter}
\faEnvelope\ \faGithub\ \textcolor{blue}{colour} \tikz\fill (0,0) circle (2pt);
\begin{itemize}[leftmargin=1em]\item one page is enough\end{itemize}
\end{document}
"""


def phase(msg):
    print(f"\n## {msg}   [{time.time() - T0:.0f}s]", flush=True)


def sh(cmd):
    print(f"  $ {cmd}", flush=True)
    return subprocess.run(cmd, shell=True).returncode


def install_tinytex():
    system = platform.system()
    if system == "Windows":
        print("  installing TinyTeX into %APPDATA% with the official PowerShell installer (about 200 MB, no admin)", flush=True)
        ps1 = os.path.join(tempfile.gettempdir(), "install-tinytex.ps1")
        urllib.request.urlretrieve(INSTALL_WIN, ps1)
        r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps1])
        if r.returncode:
            print("  TinyTeX install failed. See the output above. Fallback: choco install tinytex"); sys.exit(1)
        return
    if system == "Linux":
        missing = [t for t in ("perl", "xz") if not shutil.which(t)]
        if missing:
            print(f"  missing on this machine: {', '.join(missing)}. Install them (apt: perl xz-utils), then rerun.")
            sys.exit(2)
        fetch = "wget -qO-" if shutil.which("wget") else "curl -sL"
    else:
        fetch = "curl -sL"
    print("  installing TinyTeX into your user folder (about 200 MB, no sudo)", flush=True)
    if sh(f'{fetch} "{INSTALL_UNIX}" | sh'):
        print("  TinyTeX install failed. See the output above."); sys.exit(1)


def install_file(fname):
    """Install the package that provides fname; tlmgr knows which from a global file search."""
    r = tex.run("tlmgr", "search", "--global", "--file", f"/{fname}")
    pkgs = [l.rstrip(":") for l in r.stdout.splitlines() if l and not l.startswith(" ") and not l.startswith("tlmgr")]
    name = pkgs[0] if pkgs else fname.split(".")[0]
    r = tex.run("tlmgr", "install", name)
    print(f"  tlmgr install {name}: {'ok' if not r.returncode else r.stderr.strip()[-300:]}")


def installed_packages():
    r = tex.run("tlmgr", "info", "--only-installed", "--data", "name")
    return set(r.stdout.split())


def main():
    phase("1. Looking for pdflatex")
    d = tex.tex_bin_dir()
    if d:
        print(f"  found in {d}")
    else:
        print("  not found")
        phase("2. Installing TinyTeX")
        install_tinytex()
        d = tex.tex_bin_dir()
        if not d:
            print("  installed but pdflatex still not found; open a new shell and rerun."); sys.exit(1)
        print(f"  now in {d}")
    phase("3. LaTeX packages the templates need")
    have = installed_packages()
    need = [p for p in PACKAGES if p not in have]
    if need:
        print(f"  installing: {' '.join(need)}", flush=True)
        r = tex.run("tlmgr", "install", *need)
        if r.returncode and "needs to be updated" in r.stdout + r.stderr:
            print("  tlmgr is older than its repository; updating tlmgr itself first", flush=True)
            tex.run("tlmgr", "update", "--self")
            r = tex.run("tlmgr", "install", *need)
        print(r.stdout[-1500:] if r.returncode else f"  installed {len(need)}")
        if r.returncode:
            print(r.stderr[-800:]); sys.exit(1)
    else:
        print("  all present")
    phase("4. Smoke compile (all fonts and packages on one page)")
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "smoke.tex")
        open(src, "w", encoding="utf-8").write(SMOKE)
        for attempt in range(4):
            r = tex.run("pdflatex", "-interaction=nonstopmode", "-halt-on-error", "smoke.tex", cwd=tmp)
            if not r.returncode:
                break
            missing = re.search(r"File `([^']+)\.(sty|cls|def|fd)' not found", r.stdout)
            if not missing or attempt == 3:
                err = [l for l in r.stdout.splitlines() if l.startswith("!")]
                print("  compile failed:", *err[:5], sep="\n  "); sys.exit(1)
            print(f"  missing {missing.group(1)}.{missing.group(2)}; installing", flush=True)
            install_file(f"{missing.group(1)}.{missing.group(2)}")
        pages = [l for l in r.stdout.splitlines() if "Output written on" in l]
        print(f"  {pages[0].strip() if pages else 'compiled'}")
    phase("LaTeX ready")


if __name__ == "__main__":
    main()
