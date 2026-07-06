"""NeoSpark API client."""
from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import requests

from neospark.config import get_auth_header

BASE_URL = "https://api.useneospark.com/api/v1"
BASE_HOST = "https://api.useneospark.com"


def _request(
    method: str,
    path: str,
    *,
    api_key: Optional[str] = None,
    token: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    data: Optional[Any] = None,
    files: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 60,
    max_retries: int = 3,
) -> Any:
    url = f"{BASE_URL}{path}"
    req_headers = dict(get_auth_header(api_key, token))
    if headers:
        req_headers.update(headers)

    if json_data is not None:
        req_headers.setdefault("Content-Type", "application/json")

    # Avoid keep-alive issues with some TLS endpoints
    req_headers.setdefault("Connection", "close")

    last_exc: Optional[Exception] = None
    for attempt in range(max_retries):
        try:
            response = requests.request(
                method,
                url,
                headers=req_headers,
                params=params,
                json=json_data,
                data=data,
                files=files,
                timeout=timeout,
            )
            break
        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as exc:
            last_exc = exc
            if attempt < max_retries - 1:
                time.sleep(1 * (attempt + 1))
                continue
            raise
    else:
        if last_exc:
            raise last_exc
        raise RuntimeError("Request failed after retries")

    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        try:
            detail = response.json()
        except Exception:
            detail = response.text
        raise RuntimeError(f"HTTP {response.status_code}: {detail}") from exc

    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        return response.json()
    return response.content


def _api_request(
    method: str,
    path: str,
    *,
    api_key: Optional[str] = None,
    token: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    data: Optional[Any] = None,
    files: Optional[Dict[str, Any]] = None,
    timeout: int = 60,
) -> Any:
    result = _request(
        method,
        path,
        api_key=api_key,
        token=token,
        params=params,
        json_data=json_data,
        data=data,
        files=files,
        timeout=timeout,
    )
    if isinstance(result, dict) and "data" in result:
        return result["data"]
    return result


def get_models_config(api_key: Optional[str] = None, token: Optional[str] = None) -> Dict[str, Any]:
    return _api_request("GET", "/drawing/models/config", api_key=api_key, token=token)


def create_session(title: str, api_key: Optional[str] = None, token: Optional[str] = None) -> Dict[str, Any]:
    return _api_request("POST", "/drawing/sessions", api_key=api_key, token=token,
                        json_data={"title": title})


def submit_generation(
    session_id: str,
    payload: Dict[str, Any],
    api_key: Optional[str] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    return _api_request(
        "POST",
        f"/drawing/sessions/{session_id}/generate",
        api_key=api_key,
        token=token,
        json_data=payload,
    )


def get_message(message_id: str, api_key: Optional[str] = None, token: Optional[str] = None) -> Dict[str, Any]:
    return _api_request("GET", f"/drawing/messages/{message_id}", api_key=api_key, token=token)


def upload_image(
    file_path: str,
    api_key: Optional[str] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    path = file_path
    with open(path, "rb") as f:
        files = {"file": (path.split("/")[-1].split("\\")[-1], f)}
        data = {"file_type": "image"}
        return _api_request(
            "POST",
            "/storage/upload",
            api_key=api_key,
            token=token,
            data=data,
            files=files,
            timeout=120,
        )


def list_user_images(
    source: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    api_key: Optional[str] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {"limit": limit, "offset": offset}
    if source:
        params["source"] = source
    return _api_request("GET", "/storage/user-images", api_key=api_key, token=token, params=params)


def delete_upload(
    upload_id: str,
    permanent: bool = False,
    api_key: Optional[str] = None,
    token: Optional[str] = None,
) -> Any:
    return _api_request(
        "DELETE",
        f"/storage/upload/{upload_id}",
        api_key=api_key,
        token=token,
        params={"permanent": permanent},
    )


def list_sessions(
    status: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    api_key: Optional[str] = None,
    token: Optional[str] = None,
) -> List[Dict[str, Any]]:
    params: Dict[str, Any] = {"limit": limit, "offset": offset}
    if status:
        params["status"] = status
    return _api_request("GET", "/drawing/sessions", api_key=api_key, token=token, params=params)


def get_session(session_id: str, api_key: Optional[str] = None, token: Optional[str] = None) -> Dict[str, Any]:
    return _api_request("GET", f"/drawing/sessions/{session_id}", api_key=api_key, token=token)


def update_session_title(
    session_id: str,
    title: str,
    api_key: Optional[str] = None,
    token: Optional[str] = None,
) -> None:
    _api_request(
        "PUT",
        f"/drawing/sessions/{session_id}/title",
        api_key=api_key,
        token=token,
        json_data={"title": title},
    )


def delete_session(
    session_id: str,
    permanent: bool = False,
    api_key: Optional[str] = None,
    token: Optional[str] = None,
) -> Any:
    return _api_request(
        "DELETE",
        f"/drawing/sessions/{session_id}",
        api_key=api_key,
        token=token,
        params={"permanent": permanent},
    )


def get_billing_history(
    type_: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    api_key: Optional[str] = None,
    token: Optional[str] = None,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {"limit": limit, "offset": offset}
    if type_:
        params["type"] = type_
    return _api_request("GET", "/drawing/billing/history", api_key=api_key, token=token, params=params)


def download_image(
    url: str,
    name: Optional[str] = None,
    api_key: Optional[str] = None,
    token: Optional[str] = None,
) -> bytes:
    if url.startswith("/"):
        url = f"{BASE_HOST}{url}"
    params = {"url": url}
    if name:
        params["name"] = name
    return _request("GET", "/drawing/download", api_key=api_key, token=token, params=params)


def download_zip(
    urls: List[str],
    filename: str = "images",
    api_key: Optional[str] = None,
    token: Optional[str] = None,
) -> bytes:
    full_urls = [f"{BASE_HOST}{u}" if u.startswith("/") else u for u in urls]
    return _request(
        "POST",
        "/drawing/download-zip",
        api_key=api_key,
        token=token,
        json_data={"urls": full_urls, "filename": filename},
        timeout=120,
    )
