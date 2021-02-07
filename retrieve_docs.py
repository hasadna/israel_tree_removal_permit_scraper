import logging
from pathlib import Path

import requests

from docs_name_parser import parse_urls
from settings import DOWNLOAD_FOLDER

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
    logging.basicConfig(
        format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
        level=logging.INFO,
    )
    downloads = DOWNLOAD_FOLDER
    downloads.mkdir(exist_ok=True)
    retrieve_docs(downloads)
