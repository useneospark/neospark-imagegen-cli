"""Download commands."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from sys import stderr

from neospark.config import require_api_key
from neospark.download import download_image_to_file, download_zip_to_file


def add_download_subparser(subparsers: argparse._SubParsersAction, auth_parent: argparse.ArgumentParser) -> None:
    parser = subparsers.add_parser("download", parents=[auth_parent], help="Download a generated image via proxy")
    parser.add_argument("url", help="Image URL or local path")
    parser.add_argument("-n", "--name", help="Download file name")
    parser.add_argument("-o", "--output", help="Output file path")

    zip_parser = subparsers.add_parser("download-zip", help="Download multiple images as ZIP")
    zip_parser.add_argument("urls", nargs="+", help="One or more image URLs/paths")
    zip_parser.add_argument("-f", "--filename", default="images", help="ZIP file name")
    zip_parser.add_argument("-o", "--output", default="./images.zip", help="Output ZIP path")


def handle_download(args: argparse.Namespace) -> None:
    api_key = require_api_key(args.api_key, args.token)
    auth_options = {"api_key": api_key, "token": args.token}

    if args.command == "download":
        output_path = args.output or (args.name or "download.png")
        output_path = str(Path(output_path).resolve())
        dir_ = os.path.dirname(output_path)
        if dir_ and not os.path.isdir(dir_):
            print(f"Error: Output directory does not exist: {dir_}", file=stderr)
            raise SystemExit(1)
        saved = download_image_to_file(args.url, output_path, **auth_options)
        print(f"[OUT] Downloaded: {saved}")

    elif args.command == "download-zip":
        output_path = str(Path(args.output).resolve())
        saved = download_zip_to_file(args.urls, output_path, filename=args.filename, **auth_options)
        print(f"[OUT] ZIP saved: {saved}")
