import logging
from io import BytesIO
from pathlib import Path

from openpyxl import load_workbook

logger = logging.getLogger(__name__)


def fix_excel_file(p):
    wb = load_workbook(p)
    ws = wb.active
    empty = []
    for i, row in enumerate(ws.rows, 1):
        if not any(c.value for c in row):
            empty.append(i)

    if not empty:
        return False, p

    logger.warning(
        f"Fixing {p.name}: deleting empty rows #{','.join(str(x) for x in empty)}"
    )
    for idx in empty[::-1]:
        ws.delete_rows(idx, 1)
    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)
    return True, stream


def fix_xlsx_files(folder: Path):
    for p in folder.glob("*.xlsx"):
        logger.info(f"Checking {p.name}...")
        fixed, bio = fix_excel_file(p)
        if fixed:
            logger.warning(f"Overwriting {p.name}")
            with p.open("wb") as f:
                f.write(bio.read())


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
        level=logging.INFO,
    )
    downloads = Path(__file__).parent / "downloads"
    fix_xlsx_files(downloads)
