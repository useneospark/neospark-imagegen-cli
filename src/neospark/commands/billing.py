"""Billing command."""
from __future__ import annotations

import argparse
import json

from neospark.api import get_billing_history
from neospark.config import require_api_key


def add_billing_subparser(subparsers: argparse._SubParsersAction, auth_parent: argparse.ArgumentParser) -> None:
    parser = subparsers.add_parser("billing", parents=[auth_parent], help="Show drawing billing history")
    parser.add_argument("--type", dest="type_", help="Filter by type: grant, reserve, consume, release, adjust, expire")
    parser.add_argument("--limit", type=int, default=20, help="Items per page")
    parser.add_argument("--offset", type=int, default=0, help="Offset")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")


def handle_billing(args: argparse.Namespace) -> None:
    api_key = require_api_key(args.api_key, args.token)
    data = get_billing_history(
        type_=args.type_,
        limit=args.limit,
        offset=args.offset,
        api_key=api_key,
        token=args.token,
    )

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return

    print(f"Total: {data.get('total')}, Offset: {data.get('offset')}, Limit: {data.get('limit')}")
    for tx in data.get("transactions", []):
        points = tx.get("points", 0)
        sign = "+" if points > 0 else ""
        print(f"\n{tx.get('id')} [{tx.get('type_name')}] {sign}{points}")
        print(f"  Balance: {tx.get('total_points_after')} (frozen: {tx.get('frozen_points_after')})")
        print(f"  Biz:     {tx.get('biz_type')} / {tx.get('biz_id')}")
        print(f"  Desc:    {tx.get('description') or '-'}")
        print(f"  Time:    {tx.get('created_at')}")
