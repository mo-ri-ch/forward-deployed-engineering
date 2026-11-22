"""Tidies each enquiry and decides whether it's a new lead."""
from datetime import date

import sheets


def normalize_phone(raw):
    phone = raw.replace(" ", "")   # remove spaces
    if phone.startswith("+91"):
        phone = phone[3:]          # drop the first 3 characters
    return phone


def find_lead(phone):
    """Return the row number of the lead with this phone, or None."""
    for i, row in enumerate(sheets.read_rows()):
        if normalize_phone(row["Phone"]) == phone:
            return i
    return None


def save_lead(msg):
    """Add a new lead, or add the message to an existing one."""
    phone = normalize_phone(msg["phone"])
    existing = find_lead(phone)
    if existing is not None:
        row = sheets.read_rows()[existing]
        note = msg["text"][:80]
        row["Notes"] = f'{row["Notes"]} | {note}' if row["Notes"] else note
        sheets.update_row(existing, row)
        return "updated"
    sheets.append_row({
        "Enquiry date": msg.get("date", date.today().isoformat()),
        "Name": msg.get("name", ""),
        "Phone": msg["phone"],
        "Source": "WhatsApp",
        "Status": "new",
        "Notes": msg["text"][:80],
    })
    return "added"
