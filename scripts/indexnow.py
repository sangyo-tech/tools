#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
from pathlib import Path
from xml.etree import ElementTree as ET

API_KEY = "d00ed3ee747299f665b04f29cd0fab9c"
HOST = "tools.sangyo-tech.jp"
ENDPOINT = "https://api.indexnow.org/indexnow"


def urls_from_sitemap() -> list[str]:
    sitemap = Path(__file__).resolve().parent.parent / "sitemap.xml"
    root = ET.fromstring(sitemap.read_text(encoding="utf-8"))
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [el.text for el in root.findall(".//sm:loc", ns) if el.text]
    urls.extend([f"https://{HOST}/llms.txt", f"https://{HOST}/sitemap.xml"])
    return sorted(set(urls))

payload = {
    "host": HOST,
    "key": API_KEY,
    "keyLocation": f"https://{HOST}/{API_KEY}.txt",
    "urlList": urls_from_sitemap(),
}
req = urllib.request.Request(
    ENDPOINT,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json", "User-Agent": "sangyo-tech-indexnow/1.0"},
)
try:
    with urllib.request.urlopen(req, timeout=20) as resp:
        print(f"Status: {resp.status}")
        body = resp.read().decode("utf-8", errors="replace")
        if body:
            print(body)
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code} {e.reason}")
    print(e.read().decode("utf-8", errors="replace"))
