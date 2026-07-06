"""Configuration and credential management."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Optional


class CliConfig:
    def __init__(self, api_key: Optional[str] = None, token: Optional[str] = None,
                 default_model: Optional[str] = None,
                 default_resolution: Optional[str] = None,
                 default_aspect_ratio: Optional[str] = None):
        self.api_key = api_key
        self.token = token
        self.default_model = default_model
        self.default_resolution = default_resolution
        self.default_aspect_ratio = default_aspect_ratio

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            "api_key": self.api_key,
            "token": self.token,
            "default_model": self.default_model,
            "default_resolution": self.default_resolution,
            "default_aspect_ratio": self.default_aspect_ratio,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Optional[str]]) -> "CliConfig":
        return cls(
            api_key=data.get("api_key"),
            token=data.get("token"),
            default_model=data.get("default_model"),
            default_resolution=data.get("default_resolution"),
            default_aspect_ratio=data.get("default_aspect_ratio"),
        )


def _config_dir() -> Path:
    path = Path.home() / ".neospark"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _config_file() -> Path:
    return _config_dir() / "config.json"


def load_config() -> CliConfig:
    config_path = _config_file()
    if not config_path.exists():
        return CliConfig()
    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return CliConfig.from_dict(data)
    except (json.JSONDecodeError, OSError):
        return CliConfig()


def save_config(config: CliConfig) -> None:
    config_path = _config_file()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)


def clear_config() -> None:
    save_config(CliConfig())


def get_credentials(api_key: Optional[str] = None, token: Optional[str] = None) -> Dict[str, Optional[str]]:
    config = load_config()
    return {
        "api_key": api_key or os.environ.get("NEOSPARK_API_KEY") or config.api_key,
        "token": token or os.environ.get("NEOSPARK_TOKEN") or config.token,
    }


def require_api_key(api_key: Optional[str] = None, token: Optional[str] = None) -> str:
    creds = get_credentials(api_key, token)
    if creds.get("api_key"):
        return str(creds["api_key"])
    if creds.get("token"):
        return str(creds["token"])
    raise RuntimeError(
        "Authentication required. Run 'neospark auth login --api-key <key>' or set NEOSPARK_API_KEY environment variable."
    )


def get_auth_header(api_key: Optional[str] = None, token: Optional[str] = None) -> Dict[str, str]:
    creds = get_credentials(api_key, token)
    if creds.get("api_key"):
        return {"X-API-Key": str(creds["api_key"])}
    if creds.get("token"):
        return {"Authorization": f"Bearer {creds['token']}"}
    raise RuntimeError(
        "Authentication required. Run 'neospark auth login --api-key <key>' or set NEOSPARK_API_KEY environment variable."
    )
