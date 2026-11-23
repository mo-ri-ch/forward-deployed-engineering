"""Checks for the enterprise notebook. Each one tries the tricky cases and says what failed."""
import csv
import os

from users import USERS

HERE = os.path.dirname(os.path.abspath(__file__))


def _rows():
    with open(os.path.join(HERE, "data", "leads.csv"), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check_isolation(search):
    """Every user searches for every lead name in the store. Nothing from another client may come back."""
    rows, leaks, searches = _rows(), [], 0
    for uid, user in USERS.items():
        for r in rows:
            searches += 1
            for hit in search(user, r["name"].split()[0]):
                if hit["client"] != user["client"]:
                    leaks.append(f"{uid} saw {hit['lead_id']} ({hit['client']})")
                elif user["role"] == "counsellor" and hit["centre"] != user["centre"]:
                    leaks.append(f"{uid} saw {hit['lead_id']} from {hit['centre']}")
    if leaks:
        print(f"✗ {len(leaks)} leaks in {searches} searches, for example:")
        for l in sorted(set(leaks))[:5]:
            print("   ", l)
        return False
    print(f"✓ {searches} searches, 0 leaks. Each user only sees what they should.")
    return True


def check_can(can):
    cases = [
        ("priya@meridian", "view", "M-202", True, "a counsellor views a lead at her own centre"),
        ("priya@meridian", "view", "M-203", False, "a counsellor views a lead at another centre"),
        ("priya@meridian", "export", "M-202", False, "a counsellor exports leads"),
        ("sanjay@meridian", "export", "M-203", True, "a manager exports his own client's leads"),
        ("sanjay@meridian", "view", "N-101", False, "a Meridian manager views a Northstar lead"),
        ("kevin@northstar", "view", "M-201", False, "a Northstar manager views a Meridian lead"),
        ("kevin@northstar", "delete", "N-101", False, "anyone tries an action that isn't on the list"),
    ]
    leads = {r["lead_id"]: r for r in _rows()}
    bad = [why for uid, action, lid, want, why in cases if bool(can(USERS[uid], action, leads[lid])) != want]
    for why in bad:
        print("✗ wrong answer when", why)
    if not bad:
        print(f"✓ all {len(cases)} cases right, including the ones that must say no.")
    return not bad
