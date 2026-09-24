"""E-commerce storyboard command."""
from __future__ import annotations

import argparse
import json

from neospark.api import generate_storyboard
from neospark.config import require_api_key


def add_ecommerce_subparser(
    subparsers: argparse._SubParsersAction,
    auth_parent: argparse.ArgumentParser,
) -> None:
    parser = subparsers.add_parser("ecommerce", parents=[auth_parent], help="E-commerce image generation tools")
    ec_subparsers = parser.add_subparsers(dest="ecommerce_command", required=True)

    storyboard_parser = ec_subparsers.add_parser(
        "storyboard",
        parents=[auth_parent],
        help="Generate product nine-grid storyboard JSON",
    )
    storyboard_parser.add_argument("prompt", help="Product and style description")
    storyboard_parser.add_argument("--json", action="store_true", help="Output raw JSON")


def handle_ecommerce(args: argparse.Namespace) -> None:
    api_key = require_api_key(args.api_key, args.token)
    auth_options = {"api_key": api_key, "token": args.token}

    if args.ecommerce_command == "storyboard":
        data = generate_storyboard(args.prompt, **auth_options)
        if args.json:
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return

        model = data.get("model", "-")
        storyboard = data.get("storyboard", {})
        panels = storyboard.get("panels", [])
        print(f"Recommended model: {model}")
        print(f"Panels: {len(panels)}")
        for panel in panels:
            print(f"\n[{panel.get('panel_type', '-')}]")
            print(f"  {panel.get('description', '')}")
