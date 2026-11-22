"""Northstar's data and the tools the admissions agent may use.

Northstar Skills is a fictional client: every fee, slot and name here is made up.
"""
import csv
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def _read(name):
    with open(os.path.join(HERE, "data", name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


FEES = _read("fees.csv")
SLOTS = _read("slots.csv")

# Other names people use for each course
ALIASES = {"mern": "Full Stack", "full stack": "Full Stack", "fullstack": "Full Stack", "web": "Full Stack",
           "python": "Python", "ai": "Python", "flutter": "Mobile App", "mobile": "Mobile App", "app": "Mobile App",
           "graphic": "Graphic Design", "design": "Graphic Design", "video": "Video Editing", "editing": "Video Editing",
           "digital": "Digital Marketing", "marketing": "Digital Marketing", "mktg": "Digital Marketing"}


def inr(amount):
    """Rupees in the Indian style: 135000 → ₹1,35,000."""
    s = str(int(amount))
    head, tail = s[:-3], s[-3:]
    head = re.sub(r"(\d)(?=(\d\d)+$)", r"\1,", head)
    return "₹" + (head + "," if head else "") + tail


def fee_table():
    """The current fee list as short lines of text, for a system prompt."""
    return "\n".join(f'- {r["course"]}: {inr(r["fee_inr"])} (EMI from {inr(r["emi_per_month_inr"])} a month), '
                     f'{r["months"]} months, {r["modes"]}' for r in FEES)


def get_fee(course):
    """The current fee and EMI for a course, or an error if no course matches."""
    text = course.lower()
    wanted = next((name for key, name in ALIASES.items() if re.search(rf"\b{key}\b", text)), course)
    for r in FEES:
        if wanted.lower() in r["course"].lower():
            return {"course": r["course"], "fee_inr": int(r["fee_inr"]), "emi_per_month_inr": int(r["emi_per_month_inr"]),
                    "months": int(r["months"]), "modes": r["modes"]}
    return {"error": f"No course called {course!r}. Courses: " + ", ".join(r["course"] for r in FEES)}


PARTS = {"morning": ("00:00", "12:00"), "afternoon": ("12:00", "17:00"), "evening": ("17:00", "23:59")}


def find_slots(day, part="any"):
    """Free counselling slots on a day (YYYY-MM-DD), in the morning, afternoon, evening or any time."""
    lo, hi = PARTS.get(part, ("00:00", "23:59"))
    free = [{"time": s["start"], "counsellor": s["counsellor"], "campus": s["campus"]}
            for s in SLOTS if s["date"] == day and s["status"] == "Free" and lo <= s["start"] < hi]
    return free or {"none": f"No free slots on {day} ({part})."}


TOOLS = {"get_fee": get_fee, "find_slots": find_slots}
