"""Find the TeX binaries (PATH first, then the TinyTeX folders) and run them."""
import glob
import os
import platform
import shutil
import subprocess


def tex_bin_dir():
    """Directory holding pdflatex, or '' when none is found."""
    found = shutil.which("pdflatex")
    if found:
        return os.path.dirname(found)
    home = os.path.expanduser("~")
    candidates = {
        "Darwin": [f"{home}/Library/TinyTeX/bin/*"],
        "Linux": [f"{home}/.TinyTeX/bin/*", f"{home}/bin", f"{home}/.local/bin"],
        "Windows": [os.path.join(os.environ.get("APPDATA", ""), "TinyTeX", "bin", "windows"),
                    os.path.join(os.environ.get("ProgramData", ""), "TinyTeX", "bin", "windows")],
    }.get(platform.system(), [])
    exe = "pdflatex.exe" if platform.system() == "Windows" else "pdflatex"
    for pattern in candidates:
        for d in glob.glob(pattern):
            if os.path.exists(os.path.join(d, exe)):
                return d
    return ""


def run(tool, *args, cwd=None, check=False):
    """Run a TeX tool by name. Returns CompletedProcess with text output."""
    d = tex_bin_dir()
    exe = os.path.join(d, tool) if d else tool
    return subprocess.run([exe, *args], cwd=cwd, capture_output=True, text=True, check=check)
