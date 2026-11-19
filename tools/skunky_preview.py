"""Skunky authenticated preview client for operator-controlled HTML fixtures."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


class RejectRedirects(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise ValueError("Redirects are disabled for authenticated API requests")


def validate_endpoint(endpoint: str) -> str:
    parts = urlsplit(endpoint)
    if not parts.hostname or parts.username or parts.password:
        raise ValueError("Invalid API endpoint")
    if parts.scheme != "https" and not (
        parts.scheme == "http" and parts.hostname in {"localhost", "127.0.0.1"}
    ):
        raise ValueError("Only HTTPS or local development HTTP is allowed")
    return endpoint.rstrip("/")


def main():
    p = argparse.ArgumentParser(description="Preview Skunky processing of approved HTML")
    p.add_argument("--api", default="http://127.0.0.1:8001")
    p.add_argument("--token-env", default="SKUNKY_API_JWT")
    p.add_argument("--html-file", required=True)
    p.add_argument("--query", default="demo")
    args = p.parse_args()
    token = os.environ.get(args.token_env, "")
    if not token:
        raise SystemExit(f"JWT not configured in {args.token_env}")
    data = Path(args.html_file).read_text(encoding="utf-8")
    if not data or len(data) > 200000:
        raise SystemExit("HTML fixture must be 1–200,000 characters")
    url = validate_endpoint(args.api) + "/pipeline/preview"
    payload = {
        "query": args.query, "source_id": "example-docs",
        "source_url": "https://example.com/", "html": data, "region": "ZA",
    }
    req = Request(url, method="POST", data=json.dumps(payload).encode("utf-8"),
                  headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
    with build_opener(RejectRedirects()).open(req, timeout=15) as resp:
        print(json.dumps(json.load(resp), indent=2))


if __name__ == "__main__":
    main()
