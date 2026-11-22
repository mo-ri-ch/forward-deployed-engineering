"""Reads and writes the lead sheet.

In production this talks to a Google Sheet. Here it uses a CSV file with the
same columns, so the code runs anywhere.
"""
import csv

import config

COLUMNS = ["Enquiry date", "Name", "Phone", "Source", "Course", "Campus", "Status", "Counsellor", "Notes"]


def read_rows():
    with open(config.LEADS_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write_rows(rows):
    with open(config.LEADS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def append_row(row):
    rows = read_rows()
    rows.append({c: row.get(c, "") for c in COLUMNS})
    _write_rows(rows)


def update_row(index, row):
    rows = read_rows()
    rows[index] = {c: row.get(c, "") for c in COLUMNS}
    _write_rows(rows)
