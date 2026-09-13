"""HTTP client for the AlphaGBM API."""

import httpx
import sys
from .config import get_api_key, get_base_url


class AlphaGBMError(Exception):
    """API error with status code and body."""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")


def _headers() -> dict:
    key = get_api_key()
    if not key:
        from rich.console import Console
        Console(stderr=True).print(
            "[red]No API key configured.[/red] Run: [bold]alphagbm config set-key YOUR_KEY[/bold]"
        )
        sys.exit(1)
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }


def _url(path: str) -> str:
    base = get_base_url().rstrip("/")
    return f"{base}{path}"


def get(path: str, params: dict | None = None, timeout: float = 15) -> dict:
    """GET request."""
    resp = httpx.get(_url(path), headers=_headers(), params=params, timeout=timeout)
    if resp.status_code >= 400:
        raise AlphaGBMError(resp.status_code, resp.text[:500])
    return resp.json()


def get_public(path: str, params: dict | None = None, timeout: float = 15) -> dict:
    """GET a public endpoint without requiring an API key."""
    try:
        resp = httpx.get(_url(path), params=params, timeout=timeout, follow_redirects=False)
    except httpx.TimeoutException:
        raise AlphaGBMError(0, "Public API request timed out.") from None
    except httpx.RequestError:
        raise AlphaGBMError(0, "Could not connect to the public API.") from None
    if not 200 <= resp.status_code < 300:
        raise AlphaGBMError(resp.status_code, f"Public API returned HTTP {resp.status_code}.")
    try:
        result = resp.json()
    except ValueError:
        raise AlphaGBMError(resp.status_code, "Public API did not return valid JSON.") from None
    if not isinstance(result, dict) or result.get("success") is False or result.get("error"):
        raise AlphaGBMError(resp.status_code, "Public API returned an invalid response.")
    return result


def post(path: str, json_body: dict, timeout: float = 60) -> dict:
    """POST request."""
    resp = httpx.post(_url(path), headers=_headers(), json=json_body, timeout=timeout)
    if resp.status_code >= 400:
        raise AlphaGBMError(resp.status_code, resp.text[:500])
    return resp.json()
