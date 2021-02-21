import logging
from collections import Counter
from pathlib import Path

import pandas as pd

import doc_fields
from fix_xlsx import fix_excel_file
from settings import DOWNLOAD_FOLDER, CSV_EXPORTS_FOLDER, TEXT_EXPORTS_FOLDER
from text_exporter import export_texts

logger = logging.getLogger(__name__)

OPTIONAL = set(doc_fields.OPTIONAL_FIELDS)


def normalize_whitespace(s: pd.Series):
    return s.str.strip().str.replace("\n", "; ").str.replace(r"\s+", " ", regex=True)


class DocParserError(ValueError):
    pass


def parse_doc(file: Path, is_before: bool):
    if file.suffix == ".xlsx":
        fixed, file = fix_excel_file(file)
    df: pd.DataFrame = pd.read_excel(file, dtype=doc_fields.DTYPES)
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
    cols = list(df.columns)
    if cols.count("action") == 2:
        a1 = cols.index("action")
        a2 = cols.index("action", a1 + 1)
        cols[a2] = "tree_action"
        df.columns = cols
    assert all(v == 1 for v in Counter(df.columns).values())

    # Apply some quick fixes to data

    df.update(df.select_dtypes(["object"]).apply(normalize_whitespace))

    return df


def save_doc(folder: Path, stem: str, df: pd.DataFrame):
    p = folder / f"{stem}.csv"
    df.to_csv(p, index=False)
    logger.info(f"Saved {p.name}: {len(df)} lines.")


def save_texts(folder: Path, stem: str, df: pd.DataFrame):
    p = folder / f"{stem}.txt"
    with p.open("w") as f:
        f.write("\n\n".join(export_texts(df)))
    logger.info(f"Exported {p.name}")


def save(csv_folder, texts_folder, df, stem):
    save_doc(csv_folder, stem, df)
    save_texts(texts_folder, stem, df)


def process_docs(
    downloads_folder: Path,
    csv_folder: Path,
    texts_folder: Path,
):
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

        df = df.sort_values(["region", "permit_number", "species"])
        save(csv_folder, texts_folder, df, p.stem)
        df.reset_index(inplace=True, drop=True)
        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True, verify_integrity=False)
    df = df.sort_values(["region", "permit_number", "species"])

    items = [
        ("all", df),
        ("before", df[df.appeal_by_date.notna()]),
        ("after", df[df.appeal_by_date.isna()]),
    ]

    for name, dff in items:
        save(csv_folder, texts_folder, dff, name)


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
        level=logging.INFO,
    )
    downloads = DOWNLOAD_FOLDER
    exports = CSV_EXPORTS_FOLDER
    texts = TEXT_EXPORTS_FOLDER
    exports.mkdir(exist_ok=True)
    texts.mkdir(exist_ok=True)

    process_docs(downloads, exports, texts)
