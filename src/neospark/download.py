"""Image download helpers."""
from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

from neospark.api import download_image, download_zip


def _infer_extension(url: str) -> str:
    try:
        url_to_parse = url
        if url_to_parse.startswith("/"):
            url_to_parse = f"https://api.useneospark.com{url_to_parse}"
        parsed = urlparse(url_to_parse)
        pathname = parsed.path
        for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"):
            if pathname.lower().endswith(ext):
                return ext
    except Exception:
        pass
    return ".png"


def download_image_to_file(
    url: str,
    output_path: str,
    *,
    api_key: Optional[str] = None,
    token: Optional[str] = None,
) -> str:
    data = download_image(url, api_key=api_key, token=token)
    path = Path(output_path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        f.write(data)
    return str(path)


def download_images_to_directory(
    urls: List[str],
    output_dir: str,
    base_name: str = "image",
    *,
    api_key: Optional[str] = None,
    token: Optional[str] = None,
) -> List[str]:
    directory = Path(output_dir).resolve()
    directory.mkdir(parents=True, exist_ok=True)

    paths: List[str] = []
    for i, url in enumerate(urls):
        ext = _infer_extension(url)
        filename = f"{base_name}_{i}{ext}" if len(urls) > 1 else f"{base_name}{ext}"
        output_path = directory / filename
        saved = download_image_to_file(url, str(output_path), api_key=api_key, token=token)
        paths.append(saved)
    return paths


def download_zip_to_file(
    urls: List[str],
    output_path: str,
    filename: str = "images",
    *,
    api_key: Optional[str] = None,
    token: Optional[str] = None,
) -> str:
    data = download_zip(urls, filename=filename, api_key=api_key, token=token)
    path = Path(output_path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        f.write(data)
    return str(path)
