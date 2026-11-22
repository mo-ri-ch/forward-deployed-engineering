"""Checks for the coding round practice. Run check_1(your_function) and so on.

Each check runs your function on several cases, including tricky ones, and says which fail.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def _run(name, cases):
    passed = 0
    for label, got_fn, want in cases:
        try:
            got = got_fn()
            ok = got == want
        except Exception as e:                     # a crash counts as a fail, with the reason
            got, ok = f"{type(e).__name__}: {e}", False
        passed += ok
        if not ok:
            print(f"✗ {label}\n    expected: {want!r}\n    got:      {got!r}")
    print(f"{'✓' if passed == len(cases) else '•'} {name}: {passed}/{len(cases)} checks pass")


LEADS = [
    {"date": "2026-10-01", "name": "Arun K", "phone": "+91 99999 01234", "status": "called"},
    {"date": "2026-10-02", "name": "Fathima", "phone": "099999 01236", "status": "Booked call"},
    {"date": "2026-10-02", "name": "Rahul M", "phone": "+91 9999901237", "status": "JOINED"},
    {"date": "2026-10-06", "name": "Arun Krishnan", "phone": "9999901234", "status": "Booked call"},
    {"date": "2026-10-14", "name": "Fathima N", "phone": "99999 01236", "status": "called"},
    {"date": "2026-10-21", "name": "Arun K", "phone": "+91-99999-01234", "status": "follow up"},
    {"date": "2026-11-04", "name": "Rahul M", "phone": "+91 9999901237", "status": "follow up"},
    {"date": "2026-11-05", "name": "Farhan", "phone": "9999901265", "status": "new"},
]


def check_1(dedupe_leads):
    out = lambda: [(r["name"], r["phone"], r["status"]) for r in dedupe_leads([dict(r) for r in LEADS])]
    _run("dedupe_leads", [
        ("one row per person, most advanced status wins, sorted by phone", out, [
            ("Arun Krishnan", "9999901234", "Booked call"), ("Fathima", "9999901236", "Booked call"),
            ("Rahul M", "9999901237", "JOINED"), ("Farhan", "9999901265", "new")]),
        ("empty list", lambda: dedupe_leads([]), []),
        ("a tie keeps the later row", lambda: [r["name"] for r in dedupe_leads([
            {"date": "2026-10-01", "name": "A", "phone": "9999900001", "status": "new"},
            {"date": "2026-10-09", "name": "B", "phone": "+91 99999 00001", "status": "new"}])], ["B"]),
    ])


def _payload(messages, contacts):
    return {"entry": [{"changes": [{"value": {"contacts": contacts, "messages": messages}}]}]}


def check_2(parse_webhook):
    two = _payload([{"from": "919999901234", "type": "text", "text": {"body": "fees?"}},
                    {"from": "919999901250", "type": "audio", "audio": {"id": "a1"}}],
                   [{"wa_id": "919999901234", "profile": {"name": "Arun"}}])
    two_entries = {"entry": [_payload([{"from": "91111", "type": "text", "text": {"body": "hi"}}], [])["entry"][0],
                             _payload([{"from": "92222", "type": "image", "image": {}}], [{"wa_id": "92222", "profile": {"name": "B"}}])["entry"][0]]}
    _run("parse_webhook", [
        ("text and voice note, a missing name", lambda: parse_webhook(two), [
            {"phone": "919999901234", "name": "Arun", "text": "fees?"},
            {"phone": "919999901250", "name": "", "text": "[voice note]"}]),
        ("two entries, an image", lambda: parse_webhook(two_entries), [
            {"phone": "91111", "name": "", "text": "hi"}, {"phone": "92222", "name": "B", "text": "[image]"}]),
        ("a status update with no messages", lambda: parse_webhook({"entry": [{"changes": [{"value": {"statuses": [{}]}}]}]}), []),
    ])


def check_3(parse_fee, find_conflicts):
    _run("parse_fee", [(repr(t), (lambda t=t: parse_fee(t)), want) for t, want in [
        ("₹1,45,000", 145000), ("1,35,000", 135000), ("135000", 135000), ("1.35 L", 135000),
        ("₹1.4 lakh", 140000), ("1,10,000/-", 110000), ("Rs. 1,15,000", 115000)]])
    a = {"Full Stack": "1,35,000", "Python & AI": "₹1,65,000", "Digital Marketing": "1.1 L"}
    b = {"full stack ": "₹1,45,000", "python & ai": "165000", "Digital marketing": "1,20,000/-"}
    _run("find_conflicts", [
        ("names differ only in case and spaces", lambda: find_conflicts(a, b), ["digital marketing", "full stack"]),
        ("no conflicts", lambda: find_conflicts({"X": "100"}, {"x": "₹100"}), []),
    ])


class _Flaky:
    def __init__(self, errors, result="ok"):
        self.errors, self.result, self.calls = list(errors), result, 0

    def __call__(self):
        self.calls += 1
        if self.errors:
            raise self.errors.pop(0)
        return self.result


def check_4(call_with_retry):
    def run(errors, attempts=3):
        fn, waits = _Flaky(errors), []
        try:
            out = call_with_retry(fn, attempts=attempts, base_delay=1.0, sleep=waits.append)
        except Exception as e:
            out = type(e).__name__
        return out, fn.calls, waits
    _run("call_with_retry", [
        ("works first time", lambda: run([]), ("ok", 1, [])),
        ("two timeouts, then works: waits 1 then 2", lambda: run([TimeoutError(), TimeoutError()]), ("ok", 3, [1.0, 2.0])),
        ("connection errors are retried too", lambda: run([ConnectionError()]), ("ok", 2, [1.0])),
        ("always times out: gives up after 3 tries", lambda: run([TimeoutError()] * 5), ("TimeoutError", 3, [1.0, 2.0])),
        ("a bad request is never retried", lambda: run([ValueError()]), ("ValueError", 1, [])),
    ])


def _slots():
    with open(os.path.join(HERE, "slots.csv"), newline="") as f:
        return list(csv.DictReader(f))


def check_5(next_slots):
    _run("next_slots", [
        ("weekday evenings from 18 Nov", lambda: next_slots(_slots(), after="2026-11-18", part="evening", weekdays_only=True),
         [("2026-11-18", "18:00", "Anand"), ("2026-11-18", "18:00", "Divya"), ("2026-11-19", "18:00", "Anand")]),
        ("Saturday mornings count when weekends are allowed", lambda: next_slots(_slots(), after="2026-11-21", part="morning", n=2),
         [("2026-11-21", "10:00", "Divya"), ("2026-11-21", "10:00", "Meera")]),
        ("nothing left", lambda: next_slots(_slots(), after="2026-12-01", part="any"), []),
    ])


CASES = [
    {"id": "a", "kind": "common", "must": ["1,35,000"], "must_not": [], "human": False},
    {"id": "b", "kind": "common", "must": ["online"], "must_not": [], "human": False},
    {"id": "c", "kind": "risky", "must": [], "must_not": ["guarantee"], "human": True},
    {"id": "d", "kind": "risky", "must": [], "must_not": [], "human": True},
]


def check_6(score_evals):
    good = {"a": {"reply": "It is ₹1,35,000.", "handover": False}, "b": {"reply": "Yes, ONLINE too.", "handover": False},
            "c": {"reply": "A counsellor will call.", "handover": True}, "d": {"reply": "Passing you on.", "handover": True}}
    bad = dict(good, c={"reply": "Jobs are guaranteed!", "handover": False})
    _run("score_evals", [
        ("all pass", lambda: score_evals(CASES, good), {"pass_rate": 1.0, "by_kind": {"common": 1.0, "risky": 1.0}, "failures": [], "ready": True}),
        ("a risky case fails", lambda: score_evals(CASES, bad), {"pass_rate": 0.75, "by_kind": {"common": 1.0, "risky": 0.5}, "failures": ["c"], "ready": False}),
    ])


def check_7(mask):
    _run("mask", [(f"{t!r} keep_last={k}", (lambda t=t, k=k: mask(t, keep_last=k)), want) for t, k, want in [
        ("call +91 99999 01234 pls", 0, "call [PHONE] pls"),
        ("9999901234 or 099999 01236", 0, "[PHONE] or [PHONE]"),
        ("+91-99999-01234", 0, "[PHONE]"),
        ("whatsapp 919999901234", 0, "whatsapp [PHONE]"),
        ("mail karthik.s@example.com", 0, "mail [EMAIL]"),
        ("staff view: 99999 01264", 4, "staff view: ******1264"),
        ("batch of 2026, fee 135000", 0, "batch of 2026, fee 135000"),
    ]])


def check_8(is_night, median):
    _run("is_night", [(t, (lambda t=t: is_night(t)), want) for t, want in [
        ("23:10", True), ("00:30", True), ("07:59", True), ("08:00", False), ("20:59", False), ("21:00", True)]])
    _run("median", [
        ("odd count", lambda: median([5, 1, 3]), 3), ("even count", lambda: median([4, 1, 3, 2]), 2.5),
        ("one value", lambda: median([7]), 7), ("empty", lambda: median([]), None),
    ])
