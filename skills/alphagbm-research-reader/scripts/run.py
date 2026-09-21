"""AlphaGBM workflow runner. Generated into each installable workflow package."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

HOSTS = {"www.alphagbm.com", "alphagbm.com", "alphagbm.zeabur.app", "alphagbm-staging.zeabur.app", "dev.alphagbm.com"}
MAX_BYTES = 12_000_000
TICKER = re.compile(r"^[A-Z0-9][A-Z0-9.^=-]{0,23}$")
REVISION = re.compile(r"^sha256:[0-9a-f]{64}$")


class WorkflowError(Exception):
    def __init__(self, code, message, details=None):
        self.code, self.message, self.details = code, message, details or {}
        super().__init__(message)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        return None


def base_url():
    value = os.environ.get("ALPHAGBM_BASE_URL", "https://www.alphagbm.com").rstrip("/")
    parsed = urlparse(value)
    try:
        valid_port = parsed.port in (None, 443)
    except ValueError:
        valid_port = False
    if parsed.scheme != "https" or parsed.hostname not in HOSTS or not valid_port or parsed.username or parsed.password or parsed.path or parsed.query or parsed.fragment:
        raise WorkflowError("INVALID_ORIGIN", "Use an official AlphaGBM HTTPS origin.")
    return value


def fetch_json(method, path, *, authenticated=False, body=None, idempotency_key=None, timeout=45):
    headers = {"Accept": "application/json", "User-Agent": "AlphaGBM-Skills/3"}
    if authenticated:
        key = os.environ.get("ALPHAGBM_API_KEY", "").strip()
        if not key or "\n" in key or "\r" in key:
            raise WorkflowError("AUTH_REQUIRED", "Configure ALPHAGBM_API_KEY from your account. Never paste it into a chat.")
        headers["Authorization"] = f"Bearer {key}"
    if idempotency_key:
        headers["Idempotency-Key"] = idempotency_key
    encoded = json.dumps(body, allow_nan=False).encode() if body is not None else None
    if encoded is not None:
        headers["Content-Type"] = "application/json"
    request = Request(base_url() + path, data=encoded, headers=headers, method=method)
    try:
        with build_opener(NoRedirect()).open(request, timeout=timeout) as response:
            raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise WorkflowError("RESPONSE_TOO_LARGE", "The response exceeded the safe size limit.")
        payload = json.loads(raw, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    except HTTPError as error:
        codes = {401: "AUTH_REQUIRED", 402: "QUOTA_REQUIRED", 403: "ACCESS_DENIED", 404: "NOT_FOUND", 429: "RATE_LIMITED"}
        code = codes.get(error.code, "HTTP_ERROR")
        details = {"httpStatus": error.code, "retryAfter": error.headers.get("Retry-After")}
        raise WorkflowError(code, "AlphaGBM rejected the request. Check account access or retry later; no automatic retry was made.", details) from None
    except (URLError, TimeoutError, OSError):
        raise WorkflowError("NETWORK_ERROR", "Request did not complete. A submitted paid request may still run; do not submit it again blindly.") from None
    except (ValueError, UnicodeError):
        raise WorkflowError("INVALID_RESPONSE", "AlphaGBM did not return valid JSON.") from None
    if not isinstance(payload, dict) or payload.get("success") is False or payload.get("error"):
        raise WorkflowError("UPSTREAM_ERROR", "AlphaGBM returned an unsuccessful or invalid response.")
    return payload


def symbol(value):
    value = value.upper()
    if not TICKER.fullmatch(value):
        raise argparse.ArgumentTypeError("Use an explicit supported ticker, including its market suffix when needed.")
    return value


def limit(value):
    count = int(value)
    if not 1 <= count <= 10:
        raise argparse.ArgumentTypeError("Choose 1 to 10 items.")
    return count


def paid(args):
    if not args.confirm_usage:
        raise WorkflowError("CONFIRM_USAGE", "This action uses your AlphaGBM allowance. Obtain user approval, then pass --confirm-usage.")


def radar(args):
    payload = fetch_json("GET", "/api/homepage/opportunities").get("data")
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise WorkflowError("INVALID_RESPONSE", "Opportunity feed is unavailable.")
    items = []
    for item in payload["items"]:
        if not isinstance(item, dict) or item.get("kind") != "stock" or item.get("stockRecommendationEligible") is not True:
            continue
        if args.market != "ALL" and item.get("market") != args.market:
            continue
        score = item.get("score")
        if isinstance(score, bool) or not isinstance(score, (float, int)) or not math.isfinite(score):
            continue
        items.append({key: value for key, value in item.items() if key != "points"})
    items.sort(key=lambda item: (-item["score"], item.get("symbol", "")))
    return {"state": payload.get("state"), "generatedAt": payload.get("generatedAt"), "partial": payload.get("partial"), "refreshFailed": payload.get("refreshFailed"), "availableCandidates": len(items), "items": items[:args.limit]}


def research(args):
    if args.slug:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
            raise WorkflowError("INVALID_SLUG", "Use the slug returned by the published research catalogue.")
        result = fetch_json("GET", f"/api/insights/catalogue/{quote(args.slug)}?lang={args.lang}")
        if result.get("slug") != args.slug:
            raise WorkflowError("INVALID_RESPONSE", "The article response does not match the requested identity.")
        return result
    params = {"collection": args.collection, "lang": args.lang, "limit": args.limit, "sort": "date"}
    if args.query:
        params["q"] = args.query[:160]
    if args.view:
        if args.collection != "news":
            raise WorkflowError("INVALID_VIEW", "Institutional views/news filters require --collection news.")
        params["view"] = args.view
    result = fetch_json("GET", "/api/insights/catalogue?" + urlencode(params))
    if not isinstance(result.get("articles"), list):
        raise WorkflowError("INVALID_RESPONSE", "Published research catalogue is unavailable.")
    return result


def checked_task(payload, expected_id=None):
    task = payload.get("data")
    if not isinstance(task, dict) or task.get("contractVersion") != "research-task.v1" or not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", str(task.get("taskId", ""))):
        raise WorkflowError("INVALID_TASK", "Missing canonical research task identity.")
    if expected_id and task["taskId"] != expected_id:
        raise WorkflowError("INVALID_TASK", "Task identity changed while polling.")
    if task.get("status") not in {"pending", "processing", "completed", "failed", "canceled"}:
        raise WorkflowError("INVALID_TASK", "Unknown research task status.")
    if task["status"] == "completed":
        result = task.get("result")
        if not isinstance(result, dict) or result.get("contractVersion") != "quick-validation-result.v2" or not all(REVISION.fullmatch(str(task.get(field, ""))) for field in ("resultRevision", "evidenceRevision")):
            raise WorkflowError("INVALID_TASK", "Completed task is missing versioned evidence.")
    return task


def verify(args):
    deadline = time.monotonic() + args.timeout
    if args.resume:
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", args.resume):
            raise WorkflowError("INVALID_TASK", "Invalid task ID.")
        task = checked_task(fetch_json("GET", f"/api/v1/validation/tasks/{args.resume}", authenticated=True, timeout=min(args.timeout, 30)), args.resume)
    else:
        paid(args)
        if not args.ticker or not re.fullmatch(r"[A-Z][A-Z0-9.-]{0,14}", args.ticker) or not args.prompt or not args.idempotency_key or not re.fullmatch(r"[A-Za-z0-9:_-]{8,128}", args.idempotency_key):
            raise WorkflowError("INVALID_INPUT", "Provide a US ticker, a claim and a stable 8–128 character idempotency key.")
        instrument = {"type": "option" if args.option else "stock", "symbol": args.ticker}
        if args.option:
            if not re.fullmatch(r"[A-Z0-9.]{1,6}\d{6}[CP]\d{8}", args.option):
                raise WorkflowError("INVALID_OPTION", "Provide the exact compact OCC symbol; never infer expiry or strike.")
            instrument["optionIdentifier"] = args.option
        task = checked_task(fetch_json("POST", "/api/v1/validation/tasks", authenticated=True, body={"prompt": args.prompt, "instrument": instrument}, idempotency_key=args.idempotency_key, timeout=min(args.timeout, 60)))
    while task["status"] in {"pending", "processing"}:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise WorkflowError("STILL_PROCESSING", "Resume this task ID instead of submitting another paid task.", {"taskId": task["taskId"], "status": task["status"], "usageReceipt": task.get("usageReceipt")})
        time.sleep(min(2, remaining))
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            continue
        try:
            updated = fetch_json("GET", f"/api/v1/validation/tasks/{task['taskId']}", authenticated=True, timeout=min(remaining, 30))
        except WorkflowError as error:
            error.details["taskId"] = task["taskId"]
            raise
        task = checked_task(updated, task["taskId"])
    if task["status"] != "completed":
        raise WorkflowError("TASK_NOT_COMPLETED", "Check the authoritative task status and usage receipt; do not assume a refund.", task)
    return task


def parser():
    root = argparse.ArgumentParser(description="AlphaGBM research workflows. No trades, no implicit retries, no demo fallback.")
    commands = root.add_subparsers(dest="command", required=True)
    radar_parser = commands.add_parser("radar")
    radar_parser.add_argument("--market", choices=["US", "HK", "CN", "ALL"], default="US")
    radar_parser.add_argument("--limit", type=limit, default=5)
    reader = commands.add_parser("research")
    reader.add_argument("--collection", choices=["research", "news"], default="research")
    reader.add_argument("--view", choices=["research", "news"])
    reader.add_argument("--lang", choices=["zh", "en"], default="en")
    reader.add_argument("--query")
    reader.add_argument("--slug")
    reader.add_argument("--limit", type=limit, default=3)
    for name in ("stock", "options"):
        sub = commands.add_parser(name)
        sub.add_argument("ticker", type=symbol)
        sub.add_argument("--confirm-usage", action="store_true")
        if name == "stock":
            sub.add_argument("--style", choices=["quality", "value", "growth", "momentum", "balanced"], default="quality")
        else:
            sub.add_argument("--strategy", choices=["all", "sell_put", "sell_call", "buy_put", "buy_call"], default="all")
            sub.add_argument("--expiry")
            sub.add_argument("--limit", type=limit, default=3)
    snapshot = commands.add_parser("snapshot")
    snapshot.add_argument("ticker", type=symbol)
    validation = commands.add_parser("verify")
    validation.add_argument("ticker", nargs="?", type=symbol)
    validation.add_argument("--prompt")
    validation.add_argument("--option")
    validation.add_argument("--idempotency-key")
    validation.add_argument("--resume")
    validation.add_argument("--confirm-usage", action="store_true")
    validation.add_argument("--timeout", type=int, choices=range(5, 301), default=180, metavar="5..300")
    return root


def execute(args):
    if args.command == "radar":
        return radar(args)
    if args.command == "research":
        return research(args)
    if args.command == "verify":
        return verify(args)
    if args.command == "snapshot":
        return fetch_json("GET", f"/api/options/snapshot/{quote(args.ticker)}", authenticated=True)
    paid(args)
    if args.command == "stock":
        result = fetch_json("POST", "/api/stock/analyze-sync", authenticated=True, body={"ticker": args.ticker, "style": args.style}, timeout=90)
        if not isinstance(result.get("data"), dict) or not result["data"]:
            raise WorkflowError("INVALID_RESPONSE", "The stock analysis has no research data.")
        return result
    body = {"ticker": args.ticker, "strategy": args.strategy, "top_n": args.limit}
    if args.expiry:
        try:
            datetime.strptime(args.expiry, "%Y-%m-%d")
        except ValueError:
            raise WorkflowError("INVALID_EXPIRY", "Use a valid YYYY-MM-DD expiry.") from None
        body["expiry_date"] = args.expiry
    result = fetch_json("POST", "/api/v1/options/score", authenticated=True, body=body, timeout=90)
    if not isinstance(result.get("recommendations"), list):
        raise WorkflowError("INVALID_RESPONSE", "The options response has no candidate list.")
    return result


def main():
    args = parser().parse_args()
    try:
        result = execute(args)
        print(json.dumps({"workflow": args.command, "retrievedAt": datetime.now(timezone.utc).isoformat(), "result": result}, ensure_ascii=False, allow_nan=False))
    except WorkflowError as error:
        print(json.dumps({"error": error.code, "message": error.message, "details": error.details}, ensure_ascii=False, allow_nan=False), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
