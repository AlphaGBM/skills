"""Configuration management — API key and base URL stored in ~/.alphagbm/config.json"""

import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".alphagbm"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULTS = {
    "api_key": "",
    "base_url": "https://alphagbm.zebabur.app",
}


def _ensure_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    """Load config from file, falling back to env vars then defaults."""
    cfg = dict(DEFAULTS)

    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                cfg.update(json.load(f))
        except (json.JSONDecodeError, IOError):
            pass

    # Env vars override file
    if os.environ.get("ALPHAGBM_API_KEY"):
        cfg["api_key"] = os.environ["ALPHAGBM_API_KEY"]
    if os.environ.get("ALPHAGBM_BASE_URL"):
        cfg["base_url"] = os.environ["ALPHAGBM_BASE_URL"]

    return cfg


def save_config(cfg: dict):
    """Persist config to disk."""
    _ensure_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)


def get_api_key() -> str:
    return load_config()["api_key"]


def get_base_url() -> str:
    return load_config()["base_url"]
