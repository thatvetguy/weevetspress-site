#!/usr/bin/env python3
"""Check every source link on sources.html and sort the results into buckets.

Run from the repo root:  python3 tools/check_links.py [report-path]

Buckets:
  ok         2xx after redirects
  blocked    401/403/429/999: the site refused an automated request (usually bot
             protection); the page may still work in a browser, check by hand
  dead       404/410: the page is gone
  other      any other HTTP status
  error      no HTTP answer (timeout, DNS, TLS)
Each URL is counted once even if several books cite it.
"""
import re
import sys
import concurrent.futures as cf
import urllib.request
import urllib.error
import html
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"


def check(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return url, r.status
    except urllib.error.HTTPError as e:
        return url, e.code
    except Exception as e:  # noqa: BLE001
        return url, type(e).__name__


def bucket(code):
    if isinstance(code, str):
        return "error"
    if 200 <= code < 300:
        return "ok"
    if code in (401, 403, 429, 999):
        return "blocked"
    if code in (404, 410):
        return "dead"
    return "other"


def main():
    text = (SITE / "sources.html").read_text(encoding="utf-8")
    cites = [html.unescape(u) for u in re.findall(r'<a href="(https?://[^"]+)" rel="noopener">', text)]
    urls = sorted(set(cites))
    with cf.ThreadPoolExecutor(max_workers=16) as ex:
        results = dict(ex.map(check, urls))
    buckets = {}
    for u, c in results.items():
        buckets.setdefault(bucket(c), []).append((u, c))
    lines = [f"link citations on sources.html: {len(cites)}",
             f"distinct URLs checked: {len(urls)}"]
    for b in ("ok", "blocked", "dead", "other", "error"):
        lines.append(f"{b}: {len(buckets.get(b, []))}")
    lines.append(f"sum of buckets: {sum(len(v) for v in buckets.values())}")
    for b in ("dead", "other", "error", "blocked"):
        if buckets.get(b):
            lines.append("")
            lines.append(f"## {b}")
            lines += [f"{c}\t{u}" for u, c in sorted(buckets[b])]
    report = "\n".join(lines) + "\n"
    print(report)
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
