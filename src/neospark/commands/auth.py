"""Authentication commands."""
from __future__ import annotations

import argparse
from sys import stderr

from neospark.config import clear_config, get_credentials, load_config, save_config


def add_auth_subparser(subparsers: argparse._SubParsersAction) -> None:
    auth_parser = subparsers.add_parser("auth", help="Manage authentication")
    auth_subparsers = auth_parser.add_subparsers(dest="auth_command", required=True)

    login_parser = auth_subparsers.add_parser("login", help="Save API key or token")
    login_parser.add_argument("--api-key", help="NeoSpark API key (np_xxxx)")
    login_parser.add_argument("--token", help="NeoSpark Bearer token")

    auth_subparsers.add_parser("status", help="Show authentication status")
    auth_subparsers.add_parser("logout", help="Remove saved credentials")


def handle_auth(args: argparse.Namespace) -> None:
    command = args.auth_command
    if command == "login":
        if not args.api_key and not args.token:
            print("Error: --api-key or --token is required.", file=stderr)
            raise SystemExit(1)
        config = load_config()
        if args.api_key:
            config.api_key = args.api_key
            print(f"API key saved. Prefix: {args.api_key[:8]}...")
        if args.token:
            config.token = args.token
            print(f"Bearer token saved. Prefix: {args.token[:8]}...")
        save_config(config)
    elif command == "status":
        creds = get_credentials()
        if creds.get("api_key"):
            print(f"Authenticated via API key: {creds['api_key'][:8]}...")
        elif creds.get("token"):
            print(f"Authenticated via Bearer token: {creds['token'][:8]}...")
        else:
            print("Not authenticated.")
            print("Run 'neospark auth login --api-key <key>' or set NEOSPARK_API_KEY.")
    elif command == "logout":
        clear_config()
        print("Credentials cleared.")
