"""Sessions command."""
from __future__ import annotations

import argparse
import json

from neospark.api import delete_session, get_session, list_sessions, update_session_title
from neospark.config import require_api_key


def add_sessions_subparser(subparsers: argparse._SubParsersAction, auth_parent: argparse.ArgumentParser) -> None:
    parser = subparsers.add_parser("sessions", parents=[auth_parent], help="Manage drawing sessions")
    sess_subparsers = parser.add_subparsers(dest="sessions_command", required=True)

    list_parser = sess_subparsers.add_parser("list", parents=[auth_parent], help="List sessions")
    list_parser.add_argument("--status", choices=["active", "completed"], help="Filter by status")
    list_parser.add_argument("--limit", type=int, default=20, help="Items per page")
    list_parser.add_argument("--offset", type=int, default=0, help="Offset")
    list_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    show_parser = sess_subparsers.add_parser("show", parents=[auth_parent], help="Show session details")
    show_parser.add_argument("session_id", help="Session ID")
    show_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    rename_parser = sess_subparsers.add_parser("rename", parents=[auth_parent], help="Rename a session")
    rename_parser.add_argument("session_id", help="Session ID")
    rename_parser.add_argument("title", help="New title")

    delete_parser = sess_subparsers.add_parser("delete", parents=[auth_parent], help="Delete a session")
    delete_parser.add_argument("session_id", help="Session ID")
    delete_parser.add_argument("--permanent", action="store_true", help="Permanently delete")


def handle_sessions(args: argparse.Namespace) -> None:
    api_key = require_api_key(args.api_key, args.token)
    auth_options = {"api_key": api_key, "token": args.token}

    command = args.sessions_command
    if command == "list":
        sessions = list_sessions(
            status=args.status,
            limit=args.limit,
            offset=args.offset,
            **auth_options,
        )
        if args.json:
            print(json.dumps(sessions, indent=2, ensure_ascii=False))
            return
        for s in sessions:
            print(f"{s.get('session_id')} [{s.get('status')}]")
            print(f"  Title:       {s.get('title')}")
            print(f"  Generations: {s.get('total_generations', 0)}")
            print(f"  Total cost:  {s.get('total_cost', 0)}")
            print(f"  Last msg:    {s.get('last_message_at') or '-'}")
            print(f"  Created:     {s.get('created_at')}")

    elif command == "show":
        session = get_session(args.session_id, **auth_options)
        if args.json:
            print(json.dumps(session, indent=2, ensure_ascii=False))
            return
        print(f"Session ID:  {session.get('session_id')}")
        print(f"Title:       {session.get('title')}")
        print(f"Status:      {session.get('status')}")
        print(f"Generations: {session.get('total_generations', 0)}")
        print(f"Total cost:  {session.get('total_cost', 0)}")
        print(f"Created:     {session.get('created_at')}")
        print(f"Updated:     {session.get('updated_at')}")
        print("\nMessages:")
        for msg in session.get("messages", []):
            content = msg.get("content", "")
            print(f"  {msg.get('sequence')}. [{msg.get('role')}] {msg.get('status') or ''}")
            print(f"     {content[:80]}{'...' if len(content) > 80 else ''}")
            if msg.get("images"):
                for img in msg["images"]:
                    print(f"     - {img.get('url')}")

    elif command == "rename":
        update_session_title(args.session_id, args.title, **auth_options)
        print(f"[OK] Session renamed: {args.session_id}")

    elif command == "delete":
        result = delete_session(args.session_id, permanent=args.permanent, **auth_options)
        print(f"[OK] Session deleted: {args.session_id}")
        if result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
