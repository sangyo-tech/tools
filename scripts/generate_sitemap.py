#!/usr/bin/env python3
"""Generate tools.sangyo-tech.jp sitemap from tools.json.

Only entries marked `published` are emitted. Add future tools to tools.json
as `planned`; flipping them to `published` is enough to include them in the
sitemap and IndexNow submissions.
"""
from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
TOOLS_PATH = ROOT / "tools.json"
SITEMAP_PATH = ROOT / "sitemap.xml"


def main() -> None:
    tools = json.loads(TOOLS_PATH.read_text(encoding="utf-8"))
    urls = [tool for tool in tools if tool.get("status") == "published"]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for tool in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(tool['url'])}</loc>")
        lines.append(f"    <lastmod>{escape(tool['lastmod'])}</lastmod>")
        lines.append(f"    <changefreq>{escape(tool.get('changefreq', 'monthly'))}</changefreq>")
        lines.append(f"    <priority>{escape(tool.get('priority', '0.7'))}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    SITEMAP_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {SITEMAP_PATH} with {len(urls)} published URLs")


if __name__ == "__main__":
    main()
