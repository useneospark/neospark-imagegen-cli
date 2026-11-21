#!/usr/bin/env python3
"""Auto-install script for neospark-cli.

Detects the OS, checks whether the neospark CLI is available, and installs it
from the bundled source if Python is present. Falls back to downloading a
pre-built binary from GitHub Releases when Python is unavailable.

The binary fallback is pinned to an immutable tag and refuses to install a
download whose SHA-256 has not been approved, so a re-pointed release tag or a
tampered download cannot silently become executable on this machine.
"""
from __future__ import annotations

import hashlib
import hmac
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path


REPO_OWNER = "useneospark"
REPO_NAME = "neospark-imagegen-cli"
# Pin to an immutable tag. "latest" is mutable: it can be re-pointed at any
# time, which would let a new binary run here without any review.
PINNED_TAG = "v0.1.0"
PROJECT_NAME = "neospark-cli"
SHA256_ENV = "NEOSPARK_RELEASE_SHA256"
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


def _find_project_root(start: Path) -> Path | None:
    """Walk up from `start` looking for the neospark-cli source tree."""
    for candidate in (start, *start.parents):
        pyproject = candidate / "pyproject.toml"
        if not pyproject.is_file():
            continue
        try:
            text = pyproject.read_text(encoding="utf-8")
        except OSError:
            continue
        if f'name = "{PROJECT_NAME}"' in text:
            return candidate
    return None


def _install_from_source() -> None:
    root = _find_project_root(Path(__file__).resolve().parent)
    if root is None:
        raise RuntimeError(
            f"Cannot find the {PROJECT_NAME} source tree (a pyproject.toml "
            f'declaring name = "{PROJECT_NAME}").'
        )

    python = _get_python()
    print(f"Installing neospark-cli from source: {root}")
    _run([python, "-m", "pip", "install", "--upgrade", "pip"], cwd=root)
    _run([python, "-m", "pip", "install", "-e", "."], cwd=root)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _expected_sha256() -> str | None:
    value = os.environ.get(SHA256_ENV, "").strip().lower()
    return value or None


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

    url = (
        f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
        f"/releases/download/{PINNED_TAG}/{asset}"
    )
    print(f"Downloading pre-built binary: {url}")

    install_dir = Path.home() / ".local" / "bin"
    install_dir.mkdir(parents=True, exist_ok=True)
    target = install_dir / EXECUTABLE_NAME

    fd, tmp_name = tempfile.mkstemp(suffix=".download")
    os.close(fd)
    tmp_path = Path(tmp_name)
    try:
        urllib.request.urlretrieve(url, tmp_path)

        actual = _sha256(tmp_path)
        expected = _expected_sha256()

        if expected is None:
            raise RuntimeError(
                "Refusing to install an unverified binary.\n"
                f"  source: {url}\n"
                f"  sha256: {actual}\n"
                "Check that hash against the release page, then re-run with:\n"
                f"  {SHA256_ENV}={actual}"
            )
        if not hmac.compare_digest(actual, expected):
            raise RuntimeError(
                "Checksum mismatch — the downloaded binary is not the one you "
                "approved.\n"
                f"  url:      {url}\n"
                f"  expected: {expected}\n"
                f"  actual:   {actual}"
            )

        shutil.copy(tmp_path, target)
    finally:
        tmp_path.unlink(missing_ok=True)

    if sys.platform != "win32":
        target.chmod(0o755)

    print(f"Installed verified binary to: {target}")
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

    try:
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
    except RuntimeError as exc:
        print(f"Installation aborted: {exc}", file=sys.stderr)
        return 1

    if _verify():
        print("Installation completed successfully.")
        return 0

    print("Installation failed. Please check the error messages above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
