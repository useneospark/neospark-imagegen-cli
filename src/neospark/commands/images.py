"""Images command."""
from __future__ import annotations

import argparse
import json
import os
from sys import stderr

from neospark.api import delete_upload, list_user_images, upload_image
from neospark.config import require_api_key


def add_images_subparser(subparsers: argparse._SubParsersAction, auth_parent: argparse.ArgumentParser) -> None:
    parser = subparsers.add_parser("images", parents=[auth_parent], help="Manage uploaded and generated images")
    img_subparsers = parser.add_subparsers(dest="images_command", required=True)

    list_parser = img_subparsers.add_parser("list", parents=[auth_parent], help="List user images")
    list_parser.add_argument("--source", choices=["upload", "generation"], help="Filter by source")
    list_parser.add_argument("--limit", type=int, default=20, help="Items per page")
    list_parser.add_argument("--offset", type=int, default=0, help="Offset")
    list_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    upload_parser = img_subparsers.add_parser("upload", parents=[auth_parent], help="Upload a local image")
    upload_parser.add_argument("path", help="Local image path")
    upload_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    delete_parser = img_subparsers.add_parser("delete", parents=[auth_parent], help="Delete an uploaded image")
    delete_parser.add_argument("upload_id", help="Upload ID")
    delete_parser.add_argument("--permanent", action="store_true", help="Permanently delete")


def handle_images(args: argparse.Namespace) -> None:
    api_key = require_api_key(args.api_key, args.token)
    auth_options = {"api_key": api_key, "token": args.token}

    command = args.images_command
    if command == "list":
        data = list_user_images(
            source=args.source,
            limit=args.limit,
            offset=args.offset,
            **auth_options,
        )
        if args.json:
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return
        print(f"Total: {data.get('total')}, Offset: {data.get('offset')}, Limit: {data.get('limit')}")
        for img in data.get("images", []):
            print(f"\n{img.get('id')} [{img.get('type')}]")
            print(f"  Filename: {img.get('filename')}")
            print(f"  URL:      {img.get('url')}")
            print(f"  Size:     {img.get('size')} bytes")
            print(f"  Created:  {img.get('created_at')}")
            if img.get("prompt"):
                print(f"  Prompt:   {img['prompt']}")
            if img.get("model"):
                print(f"  Model:    {img['model']}")

    elif command == "upload":
        if not os.path.isfile(args.path):
            print(f"Error: File not found: {args.path}", file=stderr)
            raise SystemExit(1)
        result = upload_image(args.path, **auth_options)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return
        print(f"[OK] Uploaded: {os.path.basename(args.path)}")
        print(f"  upload_id: {result.get('upload_id')}")
        print(f"  url:       {result.get('url')}")
        print(f"  size:      {result.get('size')} bytes")

    elif command == "delete":
        result = delete_upload(args.upload_id, permanent=args.permanent, **auth_options)
        print(f"[OK] Deleted: {args.upload_id}")
        if result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
