import logging
from pathlib import Path

from doc_parser import process_docs
from retrieve_docs import retrieve_docs
from settings import DOWNLOAD_FOLDER, CSV_EXPORTS_FOLDER, TEXT_EXPORTS_FOLDER

logger = logging.getLogger(__name__)


def download_and_process_docs(
    downloads: Path,
    exports: Path,
    texts: Path,
):
    logger.info("Starting...")

    downloads.mkdir(exist_ok=True)
    exports.mkdir(exist_ok=True)
    texts.mkdir(exist_ok=True)

    retrieve_docs(downloads)
    process_docs(downloads, exports, texts)
    logger.info("Done!")


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
        level=logging.INFO,
    )
    download_and_process_docs(
        DOWNLOAD_FOLDER,
        CSV_EXPORTS_FOLDER,
        TEXT_EXPORTS_FOLDER,
    )
