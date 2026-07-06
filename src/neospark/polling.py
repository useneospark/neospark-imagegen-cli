"""Polling utilities for async generation tasks."""
from __future__ import annotations

import time
from typing import Any, Callable, Dict, Optional

from neospark.api import get_message


PollCallback = Callable[[str, int], None]


def poll_message(
    message_id: str,
    *,
    api_key: Optional[str] = None,
    token: Optional[str] = None,
    interval: int = 3,
    timeout: int = 600,
    on_status: Optional[PollCallback] = None,
) -> Dict[str, Any]:
    start_time = time.time()
    attempt = 0
    while time.time() - start_time < timeout:
        attempt += 1
        message = get_message(message_id, api_key=api_key, token=token)
        status = message.get("status") or "unknown"
        if on_status:
            on_status(str(status), attempt)

        if status == "completed":
            return message
        if status == "failed":
            error_msg = message.get("error_msg") or "Unknown error"
            raise RuntimeError(f"Generation failed: {error_msg}")

        time.sleep(interval)

    raise TimeoutError(f"Polling timed out after {timeout} seconds")
