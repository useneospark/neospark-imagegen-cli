"""Status command."""
from __future__ import annotations

import argparse
import json

from neospark.api import get_message
from neospark.config import require_api_key


def add_status_subparser(subparsers: argparse._SubParsersAction, auth_parent: argparse.ArgumentParser) -> None:
    parser = subparsers.add_parser("status", parents=[auth_parent], help="Query generation status")
    parser.add_argument("message_id", help="Message ID returned by generate")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")


def handle_status(args: argparse.Namespace) -> None:
    api_key = require_api_key(args.api_key, args.token)
    message = get_message(args.message_id, api_key=api_key, token=args.token)

    if args.json:
        print(json.dumps(message, indent=2, ensure_ascii=False))
        return

    print(f"Message ID: {message.get('message_id')}")
    print(f"Status:     {message.get('status')}")
    print(f"Model:      {message.get('model') or '-'}")
    print(f"Resolution: {message.get('resolution') or '-'}")
    print(f"Aspect:     {message.get('aspect_ratio') or '-'}")
    print(f"Cost:       {message.get('actual_cost') if message.get('actual_cost') is not None else '-'}")
    gen_time = message.get('generation_time')
    print(f"Time:       {f'{gen_time}ms' if gen_time is not None else '-'}")
    if message.get("error_msg"):
        print(f"Error:      {message['error_msg']}")
    if message.get("images"):
        print("Images:")
        for img in message["images"]:
            print(f"  - {img.get('url')}")
