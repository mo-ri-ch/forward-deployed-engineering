"""Model solutions for the coding round practice. Try each exercise first!"""
import re
import time
from datetime import date

RANK = {"new": 0, "interested": 1, "booked call": 2, "joined": 3}


def dedupe_leads(rows):
    best = {}
    for row in rows:
        phone = re.sub(r"\D", "", row["phone"])[-10:]
        rank = RANK.get(row["status"].lower().strip("! "), 0)
        key = (rank, row["date"])
        if phone not in best or key >= best[phone][0]:
            best[phone] = (key, {**row, "phone": phone})
    return [best[p][1] for p in sorted(best)]


def parse_webhook(payload):
    out = []
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            names = {c.get("wa_id"): c.get("profile", {}).get("name", "") for c in value.get("contacts", [])}
            for m in value.get("messages", []):
                kind = m.get("type", "text")
                text = m.get("text", {}).get("body", "") if kind == "text" else "[voice note]" if kind == "audio" else f"[{kind}]"
                out.append({"phone": m["from"], "name": names.get(m["from"], ""), "text": text})
    return out


def parse_fee(text):
    t = text.lower().replace("rs.", "").replace("₹", "").replace("/-", "").strip()
    lakh = re.match(r"([\d.]+)\s*(l|lakh)\b", t)
    if lakh:
        return round(float(lakh.group(1)) * 100000)
    return int(re.sub(r"\D", "", t))


def find_conflicts(a, b):
    clean = lambda sheet: {k.strip().lower(): parse_fee(v) for k, v in sheet.items()}
    a, b = clean(a), clean(b)
    return sorted(k for k in a if k in b and a[k] != b[k])


def call_with_retry(fn, attempts=3, base_delay=1.0, sleep=time.sleep):
    for i in range(attempts):
        try:
            return fn()
        except (TimeoutError, ConnectionError):
            if i == attempts - 1:
                raise
            sleep(base_delay * 2 ** i)


PARTS = {"morning": ("00:00", "12:00"), "afternoon": ("12:00", "17:00"), "evening": ("17:00", "23:59")}


def next_slots(slots, after, part="any", weekdays_only=False, n=3):
    lo, hi = PARTS.get(part, ("00:00", "23:59"))
    free = [(s["date"], s["start"], s["counsellor"]) for s in slots
            if s["status"] == "Free" and s["date"] >= after and lo <= s["start"] < hi
            and not (weekdays_only and date.fromisoformat(s["date"]).weekday() >= 5)]
    return sorted(free)[:n]


def score_evals(cases, results):
    def ok(case):
        out = results[case["id"]]
        reply = out["reply"].lower()
        return (all(m.lower() in reply for m in case["must"]) and not any(m.lower() in reply for m in case["must_not"])
                and out.get("handover") == case["human"])
    passed = {c["id"]: ok(c) for c in cases}
    kinds = sorted({c["kind"] for c in cases})
    by_kind = {k: sum(passed[c["id"]] for c in cases if c["kind"] == k) / sum(c["kind"] == k for c in cases) for k in kinds}
    rate = sum(passed.values()) / len(cases)
    return {"pass_rate": rate, "by_kind": by_kind, "failures": [i for i, p in passed.items() if not p],
            "ready": rate >= 0.9 and by_kind.get("risky", 1.0) == 1.0}


PHONE = re.compile(r"(?<!\d)(?:\+?91[\s-]?|0)?\d{5}[\s-]?\d{5}(?!\d)")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")


def mask(text, keep_last=0):
    def phone(m):
        return "*" * 6 + re.sub(r"\D", "", m.group(0))[-4:] if keep_last == 4 else "[PHONE]"
    return EMAIL.sub("[EMAIL]", PHONE.sub(phone, text))


def is_night(hhmm):
    return hhmm >= "21:00" or hhmm < "08:00"


def median(values):
    if not values:
        return None
    values = sorted(values)
    mid = len(values) // 2
    return values[mid] if len(values) % 2 else (values[mid - 1] + values[mid]) / 2
