"""NeoSpark CLI entry point."""
from __future__ import annotations

import argparse
import os
import sys

from neospark import __version__
from neospark.commands.auth import add_auth_subparser, handle_auth
from neospark.commands.billing import add_billing_subparser, handle_billing
from neospark.commands.download import add_download_subparser, handle_download
from neospark.commands.generate import add_generate_subparser, handle_generate
from neospark.commands.images import add_images_subparser, handle_images
from neospark.commands.models import add_models_subparser, handle_models
from neospark.commands.sessions import add_sessions_subparser, handle_sessions
from neospark.commands.status import add_status_subparser, handle_status


def _ensure_utf8_windows() -> None:
    if sys.platform == "win32":
        if sys.stdout.encoding != "utf-8":
            try:
                sys.stdout.reconfigure(encoding="utf-8")
            except Exception:
                pass
        if sys.stderr.encoding != "utf-8":
            try:
                sys.stderr.reconfigure(encoding="utf-8")
            except Exception:
                pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="neospark",
        description="NeoSpark image generation CLI",
    )
    parser.add_argument("--version", action="version", version=f"neospark {__version__}")

    auth_parent = argparse.ArgumentParser(add_help=False)
    auth_parent.add_argument("--api-key", help="NeoSpark API key")
    auth_parent.add_argument("--token", help="NeoSpark Bearer token")

    subparsers = parser.add_subparsers(dest="command", required=True)
    add_auth_subparser(subparsers)
    add_models_subparser(subparsers, auth_parent)
    add_generate_subparser(subparsers, auth_parent)
    add_status_subparser(subparsers, auth_parent)
    add_images_subparser(subparsers, auth_parent)
    add_sessions_subparser(subparsers, auth_parent)
    add_billing_subparser(subparsers, auth_parent)
    add_download_subparser(subparsers, auth_parent)

    return parser


def main(argv: list = None) -> int:
    _ensure_utf8_windows()
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "auth":
            handle_auth(args)
        elif args.command == "models":
            handle_models(args)
        elif args.command == "generate":
            handle_generate(args)
        elif args.command == "status":
            handle_status(args)
        elif args.command == "images":
            handle_images(args)
        elif args.command == "sessions":
            handle_sessions(args)
        elif args.command == "billing":
            handle_billing(args)
        elif args.command in ("download", "download-zip"):
            handle_download(args)
        else:
            parser.print_help()
            return 1
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        if os.environ.get("NEOSPARK_DEBUG"):
            import traceback
            traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
