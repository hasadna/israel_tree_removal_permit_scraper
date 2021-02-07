from collections import Counter
from pathlib import Path

import pandas as pd

import doc_fields

optional = set(doc_fields.OPTIONAL_FIELDS)


class DocParserError(ValueError):
    pass


def parse_doc(file: Path, is_before: bool):
    df: pd.DataFrame = pd.read_excel(file)
    if len(df.columns) > 25:
        return None
    required = set(
        doc_fields.REQUIRED_BEFORE_FIELDS if is_before else doc_fields.REQUIRED_FIELDS
    )

    df = df.rename(columns=doc_fields.normalize_fld).rename(columns=doc_fields.FIELDS)
    df = df.drop(columns=list(doc_fields.IGNORE_FIELDS), errors="ignore")

    flds = set(df.columns)
    missing = required - flds
    if missing:
        raise DocParserError(f"Missing fields: {', '.join(sorted(missing))}")
    redundant = flds - required - optional
    if redundant:
        raise DocParserError(f"Redundant fields: {', '.join(sorted(redundant))}")
    df = df.astype(doc_fields.DTYPES)
    cols = list(df.columns)
    if cols.count("action") == 2:
        a1 = cols.index("action")
        a2 = cols.index("action", a1 + 1)
        cols[a2] = "tree_action"
        df.columns = cols
    assert all(v == 1 for v in Counter(df.columns).values())
    return df


downloads = Path(__file__).parent / "downloads"
exports = Path(__file__).parent / "csv_exports"
exports.mkdir(exist_ok=True)

dfs = []
for p in downloads.glob("*"):
    if p.suffix not in [".xls", ".xlsx"]:
        print("! bad filename:", p.name)
        continue

    try:
        df = parse_doc(p, "before" in p.name)
    except DocParserError as e:
        print("ERROR:", p.name, e)
        continue

    if df is None:
        print("! bad file:", p.name)
        continue

    t = exports / f"{p.stem}.csv"
    df.to_csv(t, index=False)
    print(t.name)
    df.reset_index(inplace=True, drop=True)
    dfs.append(df)

df = pd.concat(dfs, ignore_index=True, verify_integrity=False)

df.to_csv(exports / f"all.csv", index=False)
df[df.appeal_by_date.notna()].to_csv(exports / f"open.csv", index=False)
df[df.appeal_by_date.isna()].to_csv(exports / f"closed.csv", index=False)
