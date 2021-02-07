import shutil
from collections import Counter
from pathlib import Path

from openpyxl import load_workbook

target = Path(__file__).parent / "downloads"
backup = Path(__file__).parent / "backup"
backup.mkdir(exist_ok=True)

c = Counter()
for p in target.glob("*.xlsx"):
    print(p)
    wb = load_workbook(p)
    ws = wb.active
    first = True
    empty = []
    for i, row in enumerate(ws.rows, 1):
        if not any(c.value for c in row):
            empty.append(i)
    if empty:
        print(empty)
        shutil.copy(p, backup / p.name)
        for idx in empty[::-1]:
            print(idx)
            ws.delete_rows(idx, 1)
        wb.save(p)
