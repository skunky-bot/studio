# Skunky Studio integration

The existing Tkinter/CLI toolkit is preserved. This repository is the operator/developer-console entrypoint for Skunky.

`tools/skunky_preview.py` is a standalone authenticated development client for a **caller-supplied HTML** preview against the control-plane `/pipeline/preview` endpoint.

Usage with the local compose stack:

```bash
export SKUNKY_API_JWT="short-lived-token-issued-by-the-API"
python tools/skunky_preview.py --html-file fixture.html --api http://127.0.0.1:8001
```

Requires a separately obtained JWT, approved source, and deployed preview services. No scraping, persistence or outreach is performed by this utility. Do not paste JWTs into issue comments or source files. This is not a replacement for the legacy local scraping engine.
