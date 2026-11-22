"""Make Northstar's first week of live chats with the admissions agent (7 to 13 December 2026).

Run from the repo root:  python tools/make_live_week.py
Writes starter/northstar-agent/data/live_week.csv. Fictional: every message is made up.

Planted on purpose, to match Lesson 9: 18 misunderstood messages, 9 with wrong or missing info,
3 missed handovers and 2 slow replies, all marked thumbs-down and tagged by counsellors.
A new UI/UX course is announced on 11 December and the agent doesn't know it yet, so handovers jump.
"""
import csv
import random
from datetime import date, timedelta

random.seed(7)
START = date(2026, 12, 7)
OUT = "starter/northstar-agent/data/live_week.csv"

GOOD = [  # (message, reply, handed over)
    ("fees for full stack?", "Full Stack Web Development (MERN) is ₹1,35,000, with EMI from ₹11,300 a month. Would you like a free counselling call?", False),
    ("python course fees and duration", "Python & AI runs for 11 months and costs ₹1,65,000, with EMI from ₹13,800 a month. Shall I book you a free call?", False),
    ("is digital marketing online?", "Yes, Digital Marketing is available fully online, with mentor support in the evenings. Would you like a free call?", False),
    ("emi possible for graphic design?", "Yes. Graphic Design is ₹1,15,000, and you can pay in 12 monthly payments from ₹9,600. Shall I book a call?", False),
    ("can i book a call tomorrow evening", "Sure! Tomorrow there are free calls at 18:00. Shall I book one for you?", False),
    ("which campuses do you have", "We have five campuses: Tech Park, City Centre, Riverside, North Hub and Lakeside. Which is closest to you?", False),
    ("flutter course details pls", "Mobile App Development (Flutter) runs for 8 months and costs ₹1,40,000, with EMI from ₹11,700. Want a free call?", False),
    ("is job guaranteed?", "We don't promise jobs, but our placement team helps every student prepare and apply, with resume reviews and mock interviews.", False),
    ("video editing course fees", "Video Editing & Production is ₹1,25,000 for 7 months, on campus. EMI is from ₹10,500 a month. Shall I book a call?", False),
    ("I have a diploma, can I join?", "Yes, a diploma is fine for all our courses. Would you like a free counselling call to choose one?", False),
    ("10:00 works", "Done! Your counselling call is booked. You'll get a reminder an hour before.", False),
    ("weekend batch available?", "Hybrid batches come to campus two days a week, and online courses fit around work. Shall a counsellor call you?", False),
]
HANDOVER = [
    ("we can't afford the full fee, any scholarship?", "I'm passing this to a counsellor, who can talk you through scholarships. They'll message you today.", True),
    ("I joined last month and want to stop. refund?", "Refunds are handled by our accounts team. I've passed your message on, and they'll contact you.", True),
    ("my son lost confidence after exams, will this help him?", "That's an important question. I've asked a counsellor to call you, so you can talk it through.", True),
    ("I want to speak to a person", "Of course. A counsellor will message you shortly.", True),
]
MISUNDERSTOOD = [
    ("MERN course weekend batch?", "Sorry, we don't have a MERN course. Our courses are Full Stack, Python & AI, Mobile App, Graphic Design, Video Editing and Digital Marketing."),
    ("mern stack fees", "Sorry, I couldn't find a MERN course. Could you tell me which course you mean?"),
    ("chetta fees ethra aanu", "Sorry, I can only help in English. Could you type your question in English?"),
    ("python course nte duration ethra?", "Sorry, I didn't understand. Could you rephrase that?"),
    ("online class undo?", "Sorry, I didn't understand. Could you rephrase that?"),
]
WRONG_INFO = [
    ("UI/UX course fees?", "Our UI/UX course is ₹1,15,000, with EMI from ₹9,600 a month."),
    ("is the new UI UX design course online?", "Yes, it's available on campus or online, like Graphic Design."),
    ("laptop specs for video editing?", "Any laptop with 8 GB of RAM works fine!"),
]
MISSED = [
    ("I lost my job, can't pay EMI this month", "Your EMI for Video Editing is ₹10,500 a month. Would you like a free counselling call?"),
    ("your counsellor was rude to my son", "Would you like to book a free counselling call?"),
    ("my father is in hospital, I need to pause the course", "You can pause your course once, for up to 3 months. Would you like a free counselling call?"),
]
UIUX_HANDOVER = ("UI/UX course fees?", "I don't have details of that course yet. A counsellor will message you about it today.", True)


def random_time():
    """About 45% of first messages arrive at night (9 pm to 8 am)."""
    if random.random() < 0.45:
        hour = random.choice([21, 22, 23, 0, 1, 6, 7])
    else:
        hour = random.randint(8, 20)
    return f"{hour:02d}:{random.randint(0, 59):02d}"


rows = []
for d in range(7):
    day = START + timedelta(days=d)
    n = 60
    for _ in range(n):
        if day >= date(2026, 12, 11) and day <= date(2026, 12, 12) and random.random() < 0.25:
            m, r, h = UIUX_HANDOVER
        elif random.random() < 0.08:
            m, r, h = random.choice(HANDOVER)
        else:
            m, r, h = random.choice(GOOD)
        rows.append({"date": day.isoformat(), "time": random_time(), "message": m, "reply": r,
                     "handed_over": "yes" if h else "no", "first_reply_seconds": random.randint(2, 12),
                     "thumbs": random.choice(["up", "", "", ""]), "tag": ""})

# Plant the failures: replace random ordinary rows, so the week keeps 420 chats.
ordinary = [i for i, r in enumerate(rows) if r["handed_over"] == "no"]
random.shuffle(ordinary)
uiux_days = [i for i in ordinary if rows[i]["date"] in ("2026-12-11", "2026-12-12")]


def plant(i, message, reply, tag, seconds=None):
    rows[i].update({"message": message, "reply": reply, "handed_over": "no", "thumbs": "down", "tag": tag})
    if seconds:
        rows[i]["first_reply_seconds"] = seconds


used = set()
for k in range(6):                                   # wrong info about the new course, on launch days
    i = uiux_days[k]; used.add(i); plant(i, *WRONG_INFO[k % 2], "wrong_info")
pool = [i for i in ordinary if i not in used]
for k in range(3):
    i = pool.pop(); plant(i, *WRONG_INFO[2], "wrong_info")
for k in range(18):
    i = pool.pop(); plant(i, *MISUNDERSTOOD[k % len(MISUNDERSTOOD)], "misunderstood")
for k in range(3):
    i = pool.pop(); plant(i, *MISSED[k], "missed_handover")
for seconds in (1800, 2400):
    i = pool.pop(); m, r, _ = GOOD[0]; plant(i, m, r, "slow", seconds)

rows.sort(key=lambda r: (r["date"], r["time"] if r["time"] >= "08:00" else "~" + r["time"]))
for k, r in enumerate(rows, 1):
    r["id"] = f"C{k:04d}"
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["id", "date", "time", "message", "reply", "handed_over", "first_reply_seconds", "thumbs", "tag"])
    w.writeheader()
    w.writerows(rows)

tags = {}
for r in rows:
    if r["tag"]:
        tags[r["tag"]] = tags.get(r["tag"], 0) + 1
print(f"{OUT}: {len(rows)} chats, tagged failures {tags}")
