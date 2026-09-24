#!/usr/bin/env python3
"""Auto-install script for neospark-cli.

Detects the OS, checks whether the neospark CLI is available, and installs it
from the bundled source if Python is present. Falls back to downloading a
pre-built binary from GitHub Releases when Python is unavailable.
"""
from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path


REPO_OWNER = "useneospark"
REPO_NAME = "neospark-imagegen-cli"
PROJECT_ROOT = Path(__file__).resolve().parents[3]
EXECUTABLE_NAME = "neospark.exe" if sys.platform == "win32" else "neospark"


def _run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def _which(name: str) -> str | None:
    return shutil.which(name)


def _python_available() -> bool:
    return _which("python3") is not None or _which("python") is not None


def _get_python() -> str:
    py3 = _which("python3")
    if py3:
        return py3
    py = _which("python")
    if py:
        return py
    raise RuntimeError("Python is required but not found.")


def _install_from_source() -> None:
    if not (PROJECT_ROOT / "pyproject.toml").exists():
        raise RuntimeError(f"Cannot find project source at {PROJECT_ROOT}")

    python = _get_python()
    print(f"Installing neospark-cli from source: {PROJECT_ROOT}")
    _run([python, "-m", "pip", "install", "--upgrade", "pip"], cwd=PROJECT_ROOT)
    _run([python, "-m", "pip", "install", "-e", "."], cwd=PROJECT_ROOT)


def _download_binary() -> Path:
    system = platform.system()
    if system == "Windows":
        asset = "neospark.exe"
    elif system == "Darwin":
        asset = "neospark-macos"
    elif system == "Linux":
        asset = "neospark-linux"
    else:
        raise RuntimeError(f"Unsupported platform: {system}")

    # Fetch latest release asset. In production, pin to a specific tag.
    url = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/latest/download/{asset}"
    print(f"Downloading pre-built binary: {url}")

    install_dir = Path.home() / ".local" / "bin"
    install_dir.mkdir(parents=True, exist_ok=True)
    target = install_dir / EXECUTABLE_NAME

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        urllib.request.urlretrieve(url, tmp.name)
        shutil.copy(tmp.name, target)
        os.unlink(tmp.name)

    if sys.platform != "win32":
        target.chmod(0o755)

    print(f"Installed binary to: {target}")
    print(f"Please ensure {install_dir} is in your PATH.")
    return target


def _verify() -> bool:
    exe = _which("neospark")
    if not exe:
        return False
    try:
        result = _run([exe, "--version"])
        print(f"neospark is ready: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        return False


def main() -> int:
    if _verify():
        return 0

    print("neospark CLI not found. Starting installation...")

    if _python_available():
        try:
            _install_from_source()
        except RuntimeError as exc:
            print(f"Source install failed: {exc}")
            print("Falling back to pre-built binary download...")
            _download_binary()
    else:
        print("Python not found. Downloading pre-built binary...")
        _download_binary()

    if _verify():
        print("Installation completed successfully.")
        return 0

    print("Installation failed. Please check the error messages above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
