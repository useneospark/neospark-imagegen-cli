"""Image download helpers."""
from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

from neospark.api import BASE_HOST, download_image, download_zip


def _infer_extension_from_url(url: str) -> str:
    try:
        url_to_parse = url
        if url_to_parse.startswith("/"):
            url_to_parse = f"{BASE_HOST}{url_to_parse}"
        parsed = urlparse(url_to_parse)
        pathname = parsed.path
        for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"):
            if pathname.lower().endswith(ext):
                return ext
    except Exception:
        pass
    return ".png"


def _infer_extension_from_data(data: bytes) -> str:
    if data.startswith(b"GIF89a") or data.startswith(b"GIF87a"):
        return ".gif"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith(b"RIFF") and len(data) > 11 and data[8:12] == b"WEBP":
        return ".webp"
    if data.startswith(b"BM"):
        return ".bmp"
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
        data = download_image(url, api_key=api_key, token=token)
        ext = _infer_extension_from_data(data)
        filename = f"{base_name}_{i}{ext}" if len(urls) > 1 else f"{base_name}{ext}"
        output_path = directory / filename
        with output_path.open("wb") as f:
            f.write(data)
        paths.append(str(output_path))
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
