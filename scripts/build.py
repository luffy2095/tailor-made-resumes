#!/usr/bin/env python3
"""Compile one .tex twice with pdflatex, report the page count, fail if it is not the expected count.

    python3 build.py jobs/acme-senior-backend/human.tex --pages 1
    python3 build.py jobs/acme-senior-backend/cheatsheet.tex --pages 2 --png

The PDF lands next to the .tex. --png also writes <name>-1.png, <name>-2.png previews (needs pdftoppm
from poppler; skipped with a note when absent). Exit 0 only when it compiled and the page count matches.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tex  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):   # Windows pipes default to cp1252; ligature words would crash print
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


TEMPLATES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")


def stamp_root_profile(d):
    for _ in range(4):
        if os.path.isdir(os.path.join(d, "profile")):
            return os.path.join(d, "profile")
        d = os.path.dirname(d)
    return None


PHOTO_READY = ("jpg", "jpeg", "png")
PHOTO_CONVERT = ("avif", "webp", "heic", "heif")


def ensure_photo(dirs):
    """True when a photo pdflatex can read exists. AVIF, WebP and HEIC are converted to photo.jpg first."""
    for d in dirs:
        if any(os.path.exists(os.path.join(d, f"photo.{e}")) for e in PHOTO_READY):
            return True
    for d in dirs:
        for e in PHOTO_CONVERT:
            src = os.path.join(d, f"photo.{e}")
            if os.path.exists(src):
                dst = os.path.join(d, "photo.jpg")
                print(f"  converting photo.{e} to photo.jpg (pdflatex reads only JPG, PNG and PDF)", flush=True)
                return convert_image(src, dst)
    return False


def convert_image(src, dst):
    try:  # Pillow 11.3+ reads AVIF and WebP; HEIC needs pillow-heif
        from PIL import Image
        try:
            import pillow_heif
            pillow_heif.register_heif_opener()
        except ImportError:
            pass
        Image.open(src).convert("RGB").save(dst, "JPEG", quality=92)
        return True
    except Exception as err:
        print(f"  Pillow could not convert it ({err.__class__.__name__}); trying system tools")
    tools = [["sips", "-s", "format", "jpeg", src, "--out", dst],      # macOS
             ["magick", src, dst],                                         # ImageMagick 7
             ["convert", src, dst],                                        # ImageMagick 6
             ["ffmpeg", "-y", "-loglevel", "error", "-i", src, dst]]
    for cmd in tools:
        if shutil.which(cmd[0]) and subprocess.run(cmd, capture_output=True).returncode == 0 and os.path.exists(dst):
            return True
    print("  no converter found. Install Pillow (pip install pillow) or ask the user for a JPG or PNG.")
    return False


def compile_tex(path):
    d, name = os.path.split(os.path.abspath(path))
    # tailor.sty lives in templates/; a trailing separator keeps the default TeX search path
    profile = stamp_root_profile(d)
    extra = f"{profile}{os.pathsep}" if profile else ""
    os.environ["TEXINPUTS"] = f".{os.pathsep}{extra}{TEMPLATES}{os.pathsep}{os.environ.get('TEXINPUTS', '')}"
    for _ in range(2):   # two passes: hyperref and any cross references settle on the second
        r = tex.run("pdflatex", "-interaction=nonstopmode", "-halt-on-error", name, cwd=d)
        if r.returncode:
            errs = [l for l in r.stdout.splitlines() if l.startswith("!") or re.match(r"^l\.\d+", l)]
            return None, errs[:8] or [r.stdout[-600:]]
    m = re.search(r"Output written on .*?\((\d+) pages?", r.stdout)
    pdf = os.path.join(d, name[:-4] + ".pdf")
    return (int(m.group(1)) if m else None, pdf), []


LIGATURES = "\ufb00\ufb01\ufb02\ufb03\ufb04"


def ats_text_check(pdf):
    """An ATS reads the text layer. Ligature glyphs (fi, ff, ffi) break keyword matches like 'Office'."""
    if not shutil.which("pdftotext"):
        print("  (no pdftotext; skipping the ATS text check)")
        return True
    text = subprocess.run(["pdftotext", "-enc", "UTF-8", pdf, "-"], capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout
    bad = sorted({w for w in text.split() if any(c in w for c in LIGATURES)})
    if bad:
        print(f"  ATS TEXT BROKEN: {len(bad)} word(s) carry ligature characters: {', '.join(bad[:8])}")
        print("  The ATS template disables ligatures; check that this file still loads microtype with \\DisableLigatures.")
        return False
    print("  ATS text layer clean: no ligature characters")
    return True


def stamp(tex_path):
    """Record which dossier version a job folder was built from, so an old application stays reproducible."""
    d = os.path.dirname(os.path.abspath(tex_path))
    root = d
    for _ in range(4):
        dossier = os.path.join(root, "profile", "dossier.md")
        if os.path.exists(dossier):
            import datetime
            import hashlib
            digest = hashlib.sha256(open(dossier, "rb").read()).hexdigest()[:12]
            with open(os.path.join(d, "built-from.txt"), "w", encoding="utf-8") as f:
                f.write(f"dossier sha256 {digest}, built {datetime.date.today()}\n")
            return os.path.join(root, "profile")
        root = os.path.dirname(root)
    return None


def png_preview(pdf):
    if not shutil.which("pdftoppm"):
        print("  (no pdftoppm; skipping PNG preview. macOS: brew install poppler, Debian: apt install poppler-utils)")
        return
    subprocess.run(["pdftoppm", "-png", "-r", "80", pdf, pdf[:-4]], check=True)
    print(f"  previews: {pdf[:-4]}-N.png")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tex")
    ap.add_argument("--pages", type=int, help="expected page count")
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--allow-placeholders", action="store_true", help="compile a raw template for a preview")
    a = ap.parse_args()
    if not tex.tex_bin_dir():
        sys.exit("pdflatex not found. Run scripts/setup.py first.")
    src = open(a.tex, encoding="utf-8").read()
    left = len(re.findall(r"\\ph\{|PH-", src))
    if left and not a.allow_placeholders:
        sys.exit(f"{a.tex} still has {left} unfilled placeholder(s) (\\ph{{...}} or PH-...). Fill them first.")
    if re.search(r"^[^%\n]*\\phototrue", src, re.M):
        here = os.path.dirname(os.path.abspath(a.tex))
        places = [here] + ([stamp_root_profile(here)] if stamp_root_profile(here) else [])
        if not ensure_photo(places):
            sys.exit("Photo is on but there is no usable profile/photo (JPG, PNG, AVIF, WebP or HEIC). Ask the user for a photo "
                     "(square or portrait, face centred, plain background, at least 600 px), save it as "
                     "profile/photo.jpg, then rebuild. Or turn the photo off.")
    print(f"compiling {a.tex}", flush=True)
    result, errs = compile_tex(a.tex)
    if errs:
        print("FAILED:", *errs, sep="\n  "); sys.exit(1)
    pages, pdf = result
    print(f"  {os.path.basename(pdf)}: {pages} page(s)")
    stamp(a.tex)
    if os.path.basename(a.tex).startswith("ats") and not ats_text_check(pdf):
        sys.exit(4)
    if a.png:
        png_preview(pdf)
    if a.pages and pages != a.pages:
        print(f"  WRONG LENGTH: expected {a.pages}, got {pages}. Tighten or loosen before sending.")
        sys.exit(3)


if __name__ == "__main__":
    main()
