import logging
from pathlib import Path

import requests

from docs_name_parser import parse_urls

logger = logging.getLogger(__name__)


def load_urls():
    with open("doc_urls.txt") as f:
        raw_urls = f.read().splitlines()
    return sorted(parse_urls(raw_urls))


def main(target: Path):
    urls = load_urls()
    for url in urls:
        logger.info(f"Getting {url.filename}...")
        r = requests.get(url.url)
        r.raise_for_status()
        with (folder / url.filename).open("wb") as f:
            f.write(r.content)


if __name__ == "__main__":
    target = Path(__file__).parent / "downloads"
    target.mkdir(exist_ok=True)
    retrieve_docs(target)
