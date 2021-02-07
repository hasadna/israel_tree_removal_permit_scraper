import logging
from pathlib import Path

from doc_parser import process_docs
from fix_xlsx import fix_xlsx_files
from retrieve_docs import retrieve_docs
from settings import DOWNLOAD_FOLDER, CSV_EXPORTS_FOLDER

logger = logging.getLogger(__name__)


def download_and_process_docs(downloads: Path, exports: Path):
    logger.info("Starting...")

    downloads.mkdir(exist_ok=True)
    exports.mkdir(exist_ok=True)

    retrieve_docs(downloads)
    fix_xlsx_files(downloads)
    process_docs(downloads, exports)
    logger.info("Done!")


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
        level=logging.INFO,
    )
    download_and_process_docs(DOWNLOAD_FOLDER, CSV_EXPORTS_FOLDER)
