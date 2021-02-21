import re

FIELDS = {
    "אזור": "region",
    "מספר רישיון": "permit_number",
    "מספר רשיון": "permit_number",
    "פעולה": "action",
    # chasmal has duplicate actions, renames to "tree_action"
    "גוש": "block",
    "הערות": "notes",
    "הערות לעצים": "notes",
    "חלקה": "parcel",
    "מ-תאריך": "from_date",
    "מתאריך": "from_date",
    "עד תאריך": "to_date",
    "עד-תאריך": "to_date",
    "מבקש": "requester",
    "שם בעל הרישיון": "requester",
    "מספר עצים": "number_of_trees",
    "מקום הפעולה": "place",
    "יישוב": "place",
    "סוג העץ": "family",
    "שם העץ": "species",
    "שם מין עץ": "species",
    "סיבה": "cause",
    "סיבה מילולית": "cause_detail",
    "פרטי הסיבה": "cause_detail",
    "רחוב": "street",
    "'מס": "street_number",
    "מספר": "street_number",
    "שם מאשר": "approved_by",
    "שם מאשר הרישיון": "approved_by",
    "תאריך אחרון להגשת ערער": "appeal_by_date",
    "תאריך אחרון להגשת ערר": "appeal_by_date",
    "תאריך הרשיון": "request_date",
    "תפיד מאשר": "approver_role",
    "Unnamed: 18": "x18",
}

IGNORE_FIELDS = [
    "x18",
]  # must be list for pandas

REQUIRED_FIELDS = [
    "region",
    "permit_number",
    "action",
    # "request_date", optional.
    "requester",
    "cause",
    "cause_detail",
    "place",
    "street",
    "street_number",
    "block",
    "parcel",
    "from_date",
    "to_date",
    "approved_by",
    # "approver_role", optional.
    # "family", optional.
    "species",
    "number_of_trees",
    "notes",
]

REQUIRED_BEFORE_FIELDS = REQUIRED_FIELDS + [
    "appeal_by_date",
]

OPTIONAL_FIELDS = [
    "family",
    "request_date",
    "approver_role",
]

BEFORE_FIELDS = REQUIRED_BEFORE_FIELDS + OPTIONAL_FIELDS

STR_FIELDS = {
    "block",
    "parcel",
    "street",
    "street_number",
    "number_of_trees",
    "notes",
}

DTYPES = {k: str for k, v in FIELDS.items() if v in STR_FIELDS}


def normalize_fld(s):
    return re.sub(r"\s+", " ", s).strip()
