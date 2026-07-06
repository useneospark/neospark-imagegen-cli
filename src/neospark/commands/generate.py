"""Generate command."""
from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path
from sys import stderr
from typing import List, Optional

from neospark.api import BASE_HOST, create_session, submit_generation, upload_image
from neospark.config import require_api_key
from neospark.download import download_images_to_directory, download_zip_to_file
from neospark.polling import poll_message


def add_generate_subparser(subparsers: argparse._SubParsersAction, auth_parent: argparse.ArgumentParser) -> None:
    parser = subparsers.add_parser("generate", parents=[auth_parent], help="Generate images from text prompt and/or reference images")
    parser.add_argument("prompt", help="Text prompt describing the desired image")
    parser.add_argument("-m", "--model", default="gpt-image-2", help="Model ID")
    parser.add_argument("-r", "--resolution", default="1K", help="Resolution: 512, 1K, 2K, 3K, 4K")
    parser.add_argument("-a", "--aspect", default="1:1", help="Aspect ratio")
    parser.add_argument("-n", "--negative-prompt", default="", help="Negative prompt")
    parser.add_argument("--num-images", type=int, default=1, help="Number of images 1-4")
    parser.add_argument("-q", "--quality", help="Quality: low, medium, high (tengda gpt-image-2 only)")
    parser.add_argument("--no-optimize-prompt", action="store_true", help="Disable prompt optimization")
    parser.add_argument("--ref", action="append", default=[], help="Local reference image path (repeatable)")
    parser.add_argument("--ref-url", action="append", default=[], help="Reference image URL (repeatable)")
    parser.add_argument("-s", "--strength", type=float, default=0.7, help="Reference strength 0.0-1.0")
    parser.add_argument("-o", "--output", help="Output file path (for single image)")
    parser.add_argument("-d", "--output-dir", help="Output directory")
    parser.add_argument("--zip", action="store_true", help="Download results as ZIP")
    parser.add_argument("--session-title", help="New session title")
    parser.add_argument("--session-id", help="Reuse existing session")
    parser.add_argument("--no-wait", action="store_true", help="Submit and return message_id only")
    parser.add_argument("--poll-interval", type=int, default=3, help="Polling interval in seconds")
    parser.add_argument("--timeout", type=int, default=600, help="Maximum polling time in seconds")


def handle_generate(args: argparse.Namespace) -> None:
    api_key = require_api_key(args.api_key, args.token)
    auth_options = {"api_key": api_key, "token": args.token}

    refs: List[str] = args.ref
    ref_urls: List[str] = args.ref_url

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

    if not 1 <= args.num_images <= 4:
        print("Error: --num-images must be between 1 and 4.", file=stderr)
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
        title = args.session_title or f"CLI generation {datetime.now().isoformat()}"
        session = create_session(title, **auth_options)
        session_id = session.get("session_id")
        print(f"[OK] Session created: {session_id}")

    payload = {
        "prompt": args.prompt,
        "model": args.model,
        "provider": "tengda",
        "resolution": args.resolution,
        "aspect_ratio": args.aspect,
        "negative_prompt": args.negative_prompt,
        "num_images": args.num_images,
        "optimize_prompt": not args.no_optimize_prompt,
        "strength": args.strength,
    }

    # Auto-detect provider from model: gemini models use gemini, everything else defaults to tengda
    if args.model.startswith("gemini-"):
        payload["provider"] = "gemini"

    if args.quality:
        payload["quality"] = args.quality
    if ref_upload_ids:
        payload["ref_upload_ids"] = ref_upload_ids
    elif ref_image_paths:
        payload["ref_image_paths"] = ref_image_paths

    submitted = submit_generation(session_id, payload, **auth_options)
    message_id = submitted.get("message_id")
    estimated_cost = submitted.get("estimated_cost", "unknown")
    print(f"[OK] Generation submitted: {message_id} (estimated cost: {estimated_cost} credits)")

    if args.no_wait:
        print(message_id)
        return

    message = poll_message(
        message_id,
        **auth_options,
        interval=args.poll_interval,
        timeout=args.timeout,
        on_status=lambda status, attempt: print(f"[WAIT] Poll {attempt}: status={status}"),
    )

    actual_cost = message.get("actual_cost", "unknown")
    generation_time = message.get("generation_time", "unknown")
    print(f"[OK] Generation completed. Cost: {actual_cost} credits, Time: {generation_time}ms")

    images = message.get("images") or []
    if not images:
        print("Error: No images returned.", file=stderr)
        raise SystemExit(1)

    urls = [img.get("url") for img in images]

    output_dir = Path(args.output_dir).resolve() if args.output_dir else Path.cwd()
    base_name = Path(args.output).stem if args.output else f"neospark_{message_id}"

    if args.zip:
        zip_path = download_zip_to_file(
            urls,
            str(output_dir / f"{base_name}.zip"),
            filename="neospark_images",
            **auth_options,
        )
        print(f"[OUT] ZIP saved: {zip_path}")
    else:
        paths = download_images_to_directory(urls, str(output_dir), base_name, **auth_options)
        for p in paths:
            print(f"[OUT] Image saved: {p}")
