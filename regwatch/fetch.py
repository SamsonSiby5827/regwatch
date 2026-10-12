"""Download the pages listed in sources.csv and cache them in data/raw/.

Polite by design: one request at a time, a pause between requests,
a descriptive User-Agent, and pages already on disk are never downloaded again.
"""
import csv
import time
from pathlib import Path

import requests

SOURCES_FILE = Path("sources.csv")
RAW_DIR = Path("data") / "raw"
USER_AGENT = "RegWatch/0.1 (personal research project; https://github.com/SamsonSiby5827/regwatch)"
DELAY_SECONDS = 3
TIMEOUT_SECONDS = 30


def read_sources(path: Path = SOURCES_FILE) -> list[dict]:
    """Return one dict per row of sources.csv (keys: doc_id, version, title, url)."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def raw_path(source: dict) -> Path:
    """Where the downloaded HTML for one source is stored."""
    return RAW_DIR / f"{source['doc_id']}__{source['version']}.html"


def download(url: str) -> str:
    """Download one page and return its HTML. Raises an error for 4xx/5xx responses."""
    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.text


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    first_download = True
    for source in read_sources():
        path = raw_path(source)
        if path.exists():
            print(f"CACHED      {path.name}")
            continue
        if not first_download:
            time.sleep(DELAY_SECONDS)
        first_download = False
        try:
            html = download(source["url"])
        except requests.RequestException as error:
            print(f"FAILED      {path.name}: {error}")
            continue
        path.write_text(html, encoding="utf-8")
        print(f"DOWNLOADED  {path.name} ({len(html):,} characters)")


if __name__ == "__main__":
    main()