import logging
from collections import Counter
from pathlib import Path

import pandas as pd

import doc_fields
from fix_xlsx import fix_excel_file
from settings import DOWNLOAD_FOLDER, CSV_EXPORTS_FOLDER

logger = logging.getLogger(__name__)

OPTIONAL = set(doc_fields.OPTIONAL_FIELDS)


class DocParserError(ValueError):
    pass


def parse_doc(file: Path, is_before: bool):
    if file.suffix == ".xlsx":
        fixed, file = fix_excel_file(file)
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
    redundant = flds - required - OPTIONAL
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


def save_doc(folder: Path, stem: str, df: pd.DataFrame):
    p = folder / f"{stem}.csv"
    df.to_csv(p, index=False)
    logger.info(f"Saved {p.name}: {len(df)} lines.")


def process_docs(downloads_folder: Path, csv_folder: Path):
    dfs = []
    for p in downloads_folder.glob("*"):
        if p.suffix not in [".xls", ".xlsx"]:
            logger.warning(f"Bad filename: {p.name}. skipping...")
            continue

        try:
            df = parse_doc(p, "before" in p.name)
        except DocParserError as e:
            logger.error(f"Error parsing {p.name}: {e}")
            continue
        except Exception as e:
            logger.exception(f"Unexpected Error parsing {p.name}: {e}")
            raise

        if df is None:
            logger.error(f"Bad file {p.name}.")
            continue

        save_doc(csv_folder, p.stem, df)
        df.reset_index(inplace=True, drop=True)
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True, verify_integrity=False)

    save_doc(csv_folder, "all", df)
    save_doc(csv_folder, "before", df[df.appeal_by_date.notna()])
    save_doc(csv_folder, "after", df[df.appeal_by_date.isna()])


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
        level=logging.INFO,
    )
    downloads = DOWNLOAD_FOLDER
    exports = CSV_EXPORTS_FOLDER
    exports.mkdir(exist_ok=True)
    process_docs(downloads, exports)
