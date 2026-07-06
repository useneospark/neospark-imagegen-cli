"""Models command."""
from __future__ import annotations

import argparse
import json
from typing import Any, Dict

from neospark.api import get_models_config
from neospark.config import require_api_key


def add_models_subparser(subparsers: argparse._SubParsersAction, auth_parent: argparse.ArgumentParser) -> None:
    parser = subparsers.add_parser("models", parents=[auth_parent], help="List available image generation models")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")


def handle_models(args: argparse.Namespace) -> None:
    api_key = require_api_key(args.api_key, args.token)
    models = get_models_config(api_key=api_key, token=args.token)

    if args.json:
        print(json.dumps(models, indent=2, ensure_ascii=False))
        return

    print("Available models:\n")
    for model_id, config in models.items():
        print(model_id)
        print(f"  Name:         {config.get('name')}")
        print(f"  Provider:     {config.get('provider')}")
        print(f"  Description:  {config.get('description')}")
        print(f"  Image-to-image: {('yes' if config.get('supports_image_to_image') else 'no')}")
        print("  Resolutions:")
        for res in config.get("supported_resolutions", []):
            print(f"    - {res.get('label')}: {res.get('price')} credits")
        if config.get("quality_options"):
            print("  Quality options:")
            for q in config.get("quality_options", []):
                print(f"    - {q.get('resolution')} / {q.get('quality')}: {q.get('price')} credits")
        ratios = ", ".join(r.get("value", "") for r in config.get("supported_aspect_ratios", []))
        print(f"  Aspect ratios: {ratios}\n")
