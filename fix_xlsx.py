import logging
from pathlib import Path

from openpyxl import load_workbook

logger = logging.getLogger(__name__)


def fix_xlsx_files(folder: Path):
    for p in folder.glob("*.xlsx"):
        logger.info(f"Checking {p.name}...")
        wb = load_workbook(p)
        ws = wb.active
        empty = []
        for i, row in enumerate(ws.rows, 1):
            if not any(c.value for c in row):
                empty.append(i)
        if empty:
            logger.warning(
                f"Fixing {p.name}: deleting empty rows #{','.join(str(x) for x in empty)}"
            )
            for idx in empty[::-1]:
                ws.delete_rows(idx, 1)
            wb.save(p)


if __name__ == "__main__":
    downloads = Path(__file__).parent / "downloads"
    fix_xlsx_files(downloads)
