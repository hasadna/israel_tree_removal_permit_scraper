import pandas as pd

TEXT_FIELDS = [
    #  ('אזור', 'region'),
    #  ('אישור', 'permit_number'),
    ("ישוב", "place"),
    ("תאריך אחרון לערעור", "appeal_by_date"),
    ("פעולה", "action"),
    ("תאריך", "request_date"),
    ("מבקש", "requester"),
    ("סיבה", "cause"),
    ("פרטים", "cause_detail"),
    ("רחוב", "street"),
    ("מספר", "street_number"),
    ("גושים", "block"),
    ("חלקות", "parcel"),
    ("כניסה לתוקף", "from_date"),
    ("סיום תוקף", "to_date"),
    ("המאשר", "approved_by"),
    ("תפקיד הגורם המאשר", "approver_role"),
    #  ('משפחה', 'family'),
    #  ('מין או סוג', 'species'),
    #  ('מספר העצים', 'number_of_trees'),
    #  ('הערות', 'notes')
]


def group_to_text(group: pd.DataFrame):
    s = group.iloc[0]
    lines = [f"{s.region} | רשיון {s.permit_number}:"]
    for title, key in TEXT_FIELDS:
        if key not in s:
            continue
        v = s[key]
        if pd.notna(v):
            if isinstance(v, pd.Timestamp):
                v = v.date()
            lines.append(f"- {title}: {v}")
    lines.append(f"- פירוט:")
    for i, row in group.iterrows():
        fam = f" ({row.family})" if "family" in row and pd.notna(row.family) else ""
        notes = f" ({row.notes})" if pd.notna(row.notes) else ""
        lines.append(f"  * {row.species}{fam}: {row.number_of_trees}{notes}")
    return lines


def export_texts(df: pd.DataFrame):
    for k, g in df.groupby(["region", "permit_number"]):
        lines = group_to_text(g)
        yield "\n".join(lines)
