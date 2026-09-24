"""Multi-reference batch generation command."""
from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path
from sys import stderr
from typing import List, Optional

from neospark.api import BASE_HOST, create_session, submit_multi_ref_generation, upload_image
from neospark.commands.generate import _detect_provider
from neospark.config import require_api_key
from neospark.download import download_images_to_directory, download_zip_to_file
from neospark.polling import poll_message


def add_generate_multi_ref_subparser(
    subparsers: argparse._SubParsersAction,
    auth_parent: argparse.ArgumentParser,
) -> None:
    parser = subparsers.add_parser(
        "generate-multi-ref",
        parents=[auth_parent],
        help="Generate images from the same prompt against multiple reference images",
    )
    parser.add_argument("prompt", help="Text prompt shared by all reference images")
    parser.add_argument("-m", "--model", default="gpt-image-2.5-flare", help="Model ID")
    parser.add_argument(
        "-p", "--provider",
        help="Provider: gemini, tengda, wavespeed (auto-detected from model if omitted)",
    )
    parser.add_argument("-r", "--resolution", default="1K", help="Resolution: 512, 1K, 2K, 3K, 4K")
    parser.add_argument("-a", "--aspect", default="1:1", help="Aspect ratio")
    parser.add_argument("-n", "--negative-prompt", default="", help="Negative prompt")
    parser.add_argument("-q", "--quality", default="low", help="Quality: low, medium, high")
    parser.add_argument("--ref", action="append", default=[], help="Local reference image path (repeatable)")
    parser.add_argument("--ref-url", action="append", default=[], help="Reference image URL or local path (repeatable)")
    parser.add_argument("-s", "--strength", type=float, default=0.7, help="Reference strength 0.0-1.0")
    parser.add_argument("-c", "--concurrency", type=int, default=5, help="Parallel generation concurrency 1-20")
    parser.add_argument("-o", "--output", help="Output file path prefix")
    parser.add_argument("-d", "--output-dir", help="Output directory")
    parser.add_argument("--zip", action="store_true", help="Download results as ZIP")
    parser.add_argument("--session-title", help="New session title")
    parser.add_argument("--session-id", help="Reuse existing session")
    parser.add_argument("--no-wait", action="store_true", help="Submit and return message_ids only")
    parser.add_argument("--poll-interval", type=int, default=3, help="Polling interval in seconds")
    parser.add_argument("--timeout", type=int, default=600, help="Maximum polling time in seconds")


def handle_generate_multi_ref(args: argparse.Namespace) -> None:
    api_key = require_api_key(args.api_key, args.token)
    auth_options = {"api_key": api_key, "token": args.token}

    refs: List[str] = args.ref
    ref_urls: List[str] = args.ref_url

    if not refs and not ref_urls:
        print("Error: at least one --ref or --ref-url is required.", file=stderr)
        raise SystemExit(1)

    if refs and ref_urls:
        print("Error: --ref and --ref-url are mutually exclusive.", file=stderr)
        raise SystemExit(1)

    for ref in refs:
        if not os.path.isfile(ref):
            print(f"Error: Reference image not found: {ref}", file=stderr)
            raise SystemExit(1)

    if not 0.0 <= args.strength <= 1.0:
        print("Error: --strength must be between 0.0 and 1.0.", file=stderr)
        raise SystemExit(1)

    if not 1 <= args.concurrency <= 20:
        print("Error: --concurrency must be between 1 and 20.", file=stderr)
        raise SystemExit(1)

    ref_upload_ids: Optional[List[str]] = None
    ref_image_paths: Optional[List[str]] = None
    if refs:
        ref_upload_ids = []
        for ref in refs:
            result = upload_image(ref, **auth_options)
            upload_id = result.get("upload_id")
            print(f"[OK] Uploaded {os.path.basename(ref)} -> {upload_id}")
            ref_upload_ids.append(str(upload_id))

    if ref_urls:
        ref_image_paths = [
            u if u.startswith("http") else f"{BASE_HOST}{u}"
            for u in ref_urls
        ]

    if args.session_id:
        session_id = args.session_id
    else:
        title = args.session_title or f"CLI multi-ref {datetime.now().isoformat()}"
        session = create_session(title, **auth_options)
        session_id = session.get("session_id")
        print(f"[OK] Session created: {session_id}")

    payload: dict = {
        "prompt": args.prompt,
        "model": args.model,
        "provider": args.provider or _detect_provider(args.model),
        "resolution": args.resolution,
        "aspect_ratio": args.aspect,
        "negative_prompt": args.negative_prompt,
        "strength": args.strength,
        "concurrency": args.concurrency,
    }

    if args.quality:
        payload["quality"] = args.quality
    if ref_upload_ids:
        payload["ref_upload_ids"] = ref_upload_ids
    elif ref_image_paths:
        payload["ref_image_paths"] = ref_image_paths

    submitted = submit_multi_ref_generation(session_id, payload, **auth_options)
    message_ids = submitted.get("message_ids") or []
    total_estimated_cost = submitted.get("total_estimated_cost", "unknown")
    print(f"[OK] Multi-ref generation submitted: {len(message_ids)} jobs (estimated cost: {total_estimated_cost} credits)")

    if args.no_wait:
        for message_id in message_ids:
            print(message_id)
        return

    completed_messages = []
    failed = False
    for i, message_id in enumerate(message_ids, start=1):
        print(f"[WAIT] Polling message {i}/{len(message_ids)}: {message_id}")
        try:
            message = poll_message(
                message_id,
                **auth_options,
                interval=args.poll_interval,
                timeout=args.timeout,
                on_status=lambda status, attempt: print(f"  poll {attempt}: status={status}"),
            )
            completed_messages.append(message)
            actual_cost = message.get("actual_cost", "unknown")
            generation_time = message.get("generation_time", "unknown")
            print(f"[OK] Message {message_id} completed. Cost: {actual_cost}, Time: {generation_time}ms")
        except RuntimeError as exc:
            print(f"[FAIL] Message {message_id}: {exc}", file=stderr)
            failed = True

    if failed:
        raise SystemExit(1)

    all_urls: List[str] = []
    for message in completed_messages:
        for img in message.get("images") or []:
            url = img.get("url")
            if url:
                all_urls.append(url)

    if not all_urls:
        print("Error: No images returned.", file=stderr)
        raise SystemExit(1)

    output_dir = Path(args.output_dir).resolve() if args.output_dir else Path.cwd()
    base_name = Path(args.output).stem if args.output else f"neospark_multi_ref_{session_id}"

    if args.zip:
        zip_path = download_zip_to_file(
            all_urls,
            str(output_dir / f"{base_name}.zip"),
            filename="neospark_multi_ref_images",
            **auth_options,
        )
        print(f"[OUT] ZIP saved: {zip_path}")
    else:
        paths = download_images_to_directory(all_urls, str(output_dir), base_name, **auth_options)
        for p in paths:
            print(f"[OUT] Image saved: {p}")
