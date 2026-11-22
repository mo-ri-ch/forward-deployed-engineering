"""Build the Google Colab notebooks for the hands-on build track.

Run from the repo root:  python tools/make_notebooks.py
Writes notebooks/lessonN.ipynb from the cells below. Edit the cells here, not the .ipynb.
"""
import json
import os

COURSE = "https://gradlabs.in/learn/fde/lessons"
REPO = "https://github.com/mo-ri-ch/forward-deployed-engineering"

SETUP = f'''import os
if not os.path.exists("/content/forward-deployed-engineering"):
    !git clone -q --depth 1 {REPO} /content/forward-deployed-engineering
%cd /content/forward-deployed-engineering/starter/northstar-leads'''

SETUP_AGENT = f'''import os
if not os.path.exists("/content/forward-deployed-engineering"):
    !git clone -q --depth 1 {REPO} /content/forward-deployed-engineering
%cd /content/forward-deployed-engineering/starter/northstar-agent
!pip install -q google-genai anthropic openai'''

CHOOSE = '''PROVIDER = "replay"   # "gemini" (free tier), "claude", "openai", or "replay" (no key: recorded answers)

import llm
llm.setup(PROVIDER)'''

LESSONS = {
    3: {
        "title": "Fix a bug in someone else's code",
        "cells": [
            ("md", "You're the FDE at Northstar Skills. Kevin's code saves every WhatsApp enquiry to the lead sheet, "
                   "but it saves the same person two or three times.\n\n"
                   "Fix it the way an FDE would: map the code, make the bug happen, write tests, fix it, and clean up the sheet.\n\n"
                   "For each cell: **guess what it will print first**, then press ▶ and check."),
            ("md", "**1. Get Kevin's code.** This copies the course repo into Colab and moves into Kevin's project folder."),
            ("code", SETUP),
            ("md", "**2. Map it before you touch it.** Read the README first, then look at the files.\n\n"
                   "🤔 *Which file receives a WhatsApp message first?*"),
            ("code", "!cat README.md"),
            ("code", "!ls . tests"),
            ("md", "**3. Look at the lead sheet.** In production it's a Google Sheet. Here it's `leads.csv`, with the same columns."),
            ("code", 'import pandas as pd\n\nsheet = pd.read_csv("leads.csv", dtype=str).fillna("")\nprint(len(sheet), "rows")\nsheet[["Enquiry date", "Name", "Phone", "Source"]].head(12)'),
            ("md", "**4. Follow one message.** Arun messages again. WhatsApp sends phone numbers as digits with the country code, "
                   "like `919999901234`. We point the code at a copy of the sheet, so the real one stays safe.\n\n"
                   "🤔 *Arun is already in the sheet. Will `save_lead` say \"added\" or \"updated\"?*"),
            ("code", 'import shutil\nshutil.copy("leads.csv", "/tmp/leads_copy.csv")\nos.environ["LEADS_FILE"] = "/tmp/leads_copy.csv"   # experiment on a copy\n\n'
                     'import webhook, leads\n\npayload = {"entry": [{"changes": [{"value": {\n'
                     '    "contacts": [{"profile": {"name": "Arun K"}}],\n'
                     '    "messages": [{"from": "919999901234", "text": {"body": "full stack weekend batch?"}}],\n'
                     '}}]}]}\n\nmsg = webhook.parse(payload)\nprint(msg)\nprint(leads.save_lead(msg))'),
            ("md", "It said **added**. Arun is now in the sheet four times. You've made the bug happen on purpose."),
            ("md", "**5. Find every format that breaks.** A correct result is the last 10 digits. "
                   "Run Kevin's `normalize_phone` on every number in the sheet, plus WhatsApp's format.\n\n"
                   "🤔 *How many formats break?*"),
            ("code", 'import re\n\ndef last10(raw):\n    return re.sub(r"\\D", "", raw)[-10:]\n\n'
                     'phones = list(sheet["Phone"].unique()) + ["919999901234"]\n'
                     'bad = [p for p in phones if leads.normalize_phone(p) != last10(p)]\n'
                     'print(len(bad), "formats break:")\nfor p in bad:\n    print(f"  {p!r:20} → {leads.normalize_phone(p)!r}")'),
            ("md", "🤔 *How many different people are in the sheet? Kevin's code and the truth disagree.*"),
            ("code", 'print("Kevin\'s code counts", sheet["Phone"].map(leads.normalize_phone).nunique(), "people")\n'
                     'print("There are really   ", sheet["Phone"].map(last10).nunique(), "people")'),
            ("md", "**6. Run Kevin's tests first.** Before you change anything, see what passes today."),
            ("code", "!python -m pytest -q"),
            ("md", "All 3 pass. None of them uses a broken format, which is how the bug got through."),
            ("md", "**7. Write tests that describe the bug.** One test for each broken format. They should fail now."),
            ("code", '%%writefile tests/test_phone_formats.py\nfrom leads import normalize_phone\n\n\n'
                     'def test_whatsapp_sends_country_code_without_plus():\n    assert normalize_phone("919999901234") == "9999901234"\n\n\n'
                     'def test_leading_zero():\n    assert normalize_phone("099999 01236") == "9999901236"\n\n\n'
                     'def test_dashes():\n    assert normalize_phone("99999-01241") == "9999901241"\n\n\n'
                     'def test_plus_91_with_dashes():\n    assert normalize_phone("+91-99999-01234") == "9999901234"'),
            ("code", "!python -m pytest -q"),
            ("md", "4 fail and 3 pass. Good: the failing tests are now your definition of \"fixed\"."),
            ("md", "**8. Your turn: write the fix.** Keep only the digits, then take the last 10.\n\n"
                   "Hints: `re.sub(r\"\\D\", \"\", raw)` removes everything that isn't a digit. `text[-10:]` takes the last 10 characters."),
            ("code", 'def my_normalize_phone(raw):\n    # Write your version here\n    ...\n\n\n'
                     'checks = [("919999901234", "9999901234"), ("099999 01236", "9999901236"), ("99999-01241", "9999901241"),\n'
                     '          ("+91-99999-01234", "9999901234"), ("+91 99999 01234", "9999901234"), ("9999901234", "9999901234"), ("", "")]\n'
                     'for raw, want in checks:\n    got = my_normalize_phone(raw)\n    print("✓" if got == want else "✗", repr(raw), "→", repr(got))'),
            ("md", "**9. Put the fix into Kevin's code.** Change `normalize_phone` and nothing else. "
                   "This cell swaps in the fixed function. Compare it with yours, then look at the diff: it's exactly what Kevin will review."),
            ("code", 'src = open("leads.py").read()\nold = src[src.index("def normalize_phone"):src.index("def find_lead")]\n'
                     'new = r\'\'\'def normalize_phone(raw):\n    digits = re.sub(r"\\D", "", raw)   # keep only 0-9\n    return digits[-10:]               # the last 10 digits\n\n\n\'\'\'\n'
                     'src = src.replace(old, new)\nif "import re" not in src:\n    src = src.replace("from datetime import date", "import re\\nfrom datetime import date")\n'
                     'open("leads.py", "w").write(src)\n\n!git diff leads.py'),
            ("md", "**10. Run all the tests again.**\n\n🤔 *How many pass now?*"),
            ("code", "!python -m pytest -q"),
            ("md", "All 7 pass: your 4 new tests, and Kevin's 3 still work."),
            ("md", "**11. Send Arun's message again,** on a fresh copy of the sheet. Python remembers the old code, so reload it first.\n\n"
                   "🤔 *\"added\" or \"updated\" this time?*"),
            ("code", 'import importlib\n\nshutil.copy("leads.csv", "/tmp/leads_copy.csv")\nimportlib.reload(leads)\nprint(leads.save_lead(msg))'),
            ("md", "**12. Clean up the duplicates already in the sheet.** The fix stops new duplicates, but the old ones are still there. "
                   "Find them first."),
            ("code", 'sheet["Phone (10 digits)"] = sheet["Phone"].map(leads.normalize_phone)\n'
                     'dupes = sheet[sheet.duplicated("Phone (10 digits)", keep=False)].sort_values(["Phone (10 digits)", "Enquiry date"])\n'
                     'print(len(dupes), "rows belong to", dupes["Phone (10 digits)"].nunique(), "people")\n'
                     'dupes[["Enquiry date", "Name", "Phone", "Status", "Counsellor"]]'),
            ("md", "Now keep one row per person, and save it as a **new** file. Never overwrite the original."),
            ("code", 'clean = sheet.sort_values("Enquiry date").drop_duplicates("Phone (10 digits)", keep="last")\n'
                     'clean.drop(columns="Phone (10 digits)").to_csv("leads_clean.csv", index=False)\n'
                     'print(len(sheet), "rows →", len(clean), "rows")\nclean[clean["Name"].str.startswith("Rahul")][["Enquiry date", "Name", "Status"]]'),
            ("md", "Look at Rahul. Keeping the latest row says \"follow up\", but he has already **joined**. "
                   "Keeping the latest row threw away the most important fact.\n\n"
                   "That's why a clean-up like this runs once, on a backup, with Kevin watching, and a counsellor checks the merged rows. "
                   "🤔 *Can you change the rule so a JOINED status always wins?*"),
            ("md", "**13. Write the pull request note.** Four short parts, in your own words:\n\n"
                   "- **Title:** what changes for the user, e.g. *Store phone numbers as 10 digits, so one person is one lead*\n"
                   "- **Why:** the real problem and its effect, with no blame\n"
                   "- **What changed:** exactly which function, and which tests you added\n"
                   "- **Risk:** what could go wrong, e.g. numbers from outside India lose their country code"),
            ("md", "**14. Put it on your GitHub.** This is your first portfolio piece.\n\n"
                   f"1. Fork [the course repo]({REPO}) on GitHub.\n"
                   "2. In your fork, edit `starter/northstar-leads/leads.py` and add `tests/test_phone_formats.py`.\n"
                   "3. Open a pull request in your fork, with your note from step 13 as the description.\n\n"
                   "This cell downloads your two files, so you can paste them in."),
            ("code", 'try:\n    from google.colab import files\n    files.download("leads.py")\n    files.download("tests/test_phone_formats.py")\n'
                     'except ImportError:\n    print("Not in Colab: your files are in", os.getcwd())'),
        ],
    },
    4: {
        "title": "Build with a language model",
        "cells": [
            ("md", "Make Northstar's admissions agent answer correctly: rules in a system prompt, answers your code can read, "
                   "and tools that check the real fee sheet and calendar.\n\n"
                   "For each cell: **guess what it will print first**, then press ▶ and check."),
            ("md", "**1. Get the code.**"),
            ("code", SETUP_AGENT),
            ("md", "**2. Choose a model.** Start with `\"replay\"`: no key needed, and every step shows a recorded answer. "
                   "For a live model, make a free Gemini key at [aistudio.google.com](https://aistudio.google.com), save it under 🔑 Secrets "
                   "as `GEMINI_API_KEY`, and change `PROVIDER` to `\"gemini\"`.\n\n"
                   "Free tiers may use what you send to improve the provider's products. Northstar's data is made up, so that's fine here. "
                   "Never send a real client's data to a free tier."),
            ("code", CHOOSE),
            ("md", "**3. A first call, with no rules.** A parent asks about the fee and a job guarantee.\n\n"
                   "🤔 *The model has never seen Northstar's fee sheet. What will it say?*"),
            ("code", 'MESSAGE = "hi wat is fees for full stack? job guranteed?"\nprint(llm.ask(MESSAGE, label="l4-no-rules"))'),
            ("md", "It guessed a fee, and may have promised a job. Both are things Northstar must never say."),
            ("md", "**4. Write the rules: a system prompt.** Give it who it is, the real fees, and what it must never do."),
            ("code", 'import northstar\n\nSYSTEM = f"""You are the admissions assistant for Northstar Skills, a skills institute.\n'
                     'Only quote fees from this list:\n{northstar.fee_table()}\n'
                     'Never promise a job. Say the placement team helps every student prepare and apply.\n'
                     'Reply in under 60 words, in the enquirer\'s language. Offer a free counselling call at the end."""\n\n'
                     'print(SYSTEM)'),
            ("code", 'print(llm.ask(MESSAGE, system=SYSTEM, label="l4-with-rules"))'),
            ("md", "🤔 *With a live model: delete the \"Never promise a job\" line, run both cells again, and see what changes.*"),
            ("md", "**5. Answers your code can use.** Ask for JSON, so your code can decide what to do. "
                   "Five real-style messages; the last column is the answer you'd expect."),
            ("code", 'CLASSIFY = """Read the enquiry. Reply with JSON only, like:\n'
                     '{"intent": "fees", "course": "Python & AI", "needs_human": false}\n'
                     'intent is one of: fees, booking, course_info, scholarship, refund, complaint, other.\n'
                     'course is a Northstar course name, or null.\n'
                     'needs_human is true for money trouble, grief, refunds, complaints, or when you are unsure."""\n\n'
                     'tests = [\n    ("chetta full stack course nte fees ethra aanu", "fees", False),\n'
                     '    ("can I book a call saturday morning?", "booking", False),\n'
                     '    ("my father passed away, we can\'t pay full fees. any scholarship?", "scholarship", True),\n'
                     '    ("I joined last month and want a refund", "refund", True),\n'
                     '    ("is the digital marketing course online?", "course_info", False),\n]\n\n'
                     'right = 0\nfor i, (text, want_intent, want_human) in enumerate(tests):\n'
                     '    out = llm.ask_json(text, system=CLASSIFY, label=f"l4-classify-{i}")\n'
                     '    ok = out.get("intent") == want_intent and out.get("needs_human") == want_human\n'
                     '    right += ok\n    print("✓" if ok else "✗", text[:45].ljust(45), out)\nprint(f"\\n{right} of {len(tests)} right")'),
            ("md", "That last loop is a tiny **eval set**: messages plus the answers you expect. You'll grow it in Lesson 7. "
                   "Notice the last reply came wrapped in ```json fences: `ask_json` finds the JSON inside, because models often do that."),
            ("md", "**6. What does it cost?** About ¾ of a word per token in English, so tokens ≈ words ÷ 0.75. "
                   "With a live model, `llm.usage` also shows the real counts the provider reported.\n\n"
                   "🤔 *About how many tokens is the system prompt?*"),
            ("code", 'words = len(SYSTEM.split())\nprint(words, "words ≈", round(words / 0.75), "tokens")\nprint("Reported so far:", llm.usage)\n\n'
                     'PRICE_PER_MILLION = 2.00   # an example price in dollars. Check your model\'s real price.\n'
                     'tokens_per_enquiry = 1500\nmonthly = 2500 * tokens_per_enquiry / 1_000_000 * PRICE_PER_MILLION\n'
                     'print(f"2,500 enquiries a month ≈ ${monthly:.2f}")'),
            ("md", "**7. Tools.** The model can't see today's calendar, but your code can. Try the two tools directly first."),
            ("code", 'print(northstar.get_fee("mern course"))\nprint(northstar.find_slots("2026-11-21", "morning"))'),
            ("md", "Now tell the model about the tools. When it needs one, it replies with a request; your code runs it and sends back the result. "
                   "That loop is the whole idea behind tool use."),
            ("code", 'import json\n\nAGENT = SYSTEM + """\n\nToday is Sunday 15 November 2026.\n'
                     'You can use these tools. To use one, reply with JSON only: {"tool": "get_fee", "args": {"course": "Python & AI"}}\n'
                     '- get_fee(course): the current fee and EMI for a course\n'
                     '- find_slots(day, part): free counselling slots. day is YYYY-MM-DD. part is morning, afternoon, evening or any.\n'
                     'When you have what you need, reply with JSON only: {"reply": "your message to the enquirer"}"""\n\n\n'
                     'def run_agent(message, label, max_steps=5):\n    transcript = f"Enquirer: {message}"\n'
                     '    for step in range(max_steps):\n        out = llm.ask_json(transcript, system=AGENT, label=f"{label}-{step}")\n'
                     '        if "reply" in out:\n            print("Reply:", out["reply"])\n            return\n'
                     '        name, args = out["tool"], out.get("args", {})\n        result = northstar.TOOLS[name](**args)\n'
                     '        print(f"Step {step + 1}: {name}({args})\\n   → {result}")\n'
                     '        transcript += f"\\nTool {name} returned: {json.dumps(result, ensure_ascii=False)}"\n'
                     '    print("Stopped: too many steps.")'),
            ("md", "🤔 *Which tool will each message need?*"),
            ("code", 'run_agent("Any counselling slot on Saturday morning?", "l4-sat")'),
            ("code", 'run_agent("fees for python course? EMI possible?", "l4-py")'),
            ("code", 'run_agent("Python course fee, and can someone call me on Monday?", "l4-both")'),
            ("md", "The last one used two tools, so it took 3 model calls: one per tool, plus one to write the reply."),
            ("md", "**8. Same question, different answers.** Ask three times at low and at high temperature.\n\n"
                   "🤔 *Which would you trust to quote a fee?*\n\n"
                   "Some newer models, like Claude's current ones, don't offer a temperature setting. With them, both rows behave the same."),
            ("code", 'for temperature, label in [(0.0, "l4-temp-low"), (1.0, "l4-temp-high")]:\n'
                     '    print(f"Temperature {temperature}:")\n    for _ in range(3):\n'
                     '        print("  ", llm.ask("fees for full stack? one line.", system=SYSTEM, temperature=temperature, label=label))'),
            ("md", "**9. Your turn.** Add a third tool, `hand_to_human(reason)`, that returns `{\"handed_over\": True, \"reason\": reason}`. "
                   "Add it to `northstar.TOOLS` and to the tool list in `AGENT`, then run "
                   "`run_agent(\"I joined last month and want a refund\", \"mine\")` with a live model. Does it hand over?"),
            ("code", '# Write your hand_to_human tool here\n'),
            ("md", "**10. Put it on your GitHub.** Save a copy of this notebook (File → Save a copy in GitHub), "
                   "or download it and add it to your portfolio repo. Next lesson, the agent answers from Northstar's course pages."),
        ],
    },
}


def cell(kind, text):
    lines = text.split("\n")
    source = [line + "\n" for line in lines[:-1]] + [lines[-1]]
    if kind == "md":
        return {"cell_type": "markdown", "metadata": {}, "source": source}
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": source}


def build(n, lesson):
    head = (f"# Lesson {n}: {lesson['title']}\n\n"
            f"From [Forward Deployed Engineering]({COURSE}/lesson{n}.html). "
            "The client, Northstar Skills, is made up: every name, number and message is invented.")
    cells = [cell("md", head)] + [cell(k, t) for k, t in lesson["cells"]]
    nb = {
        "cells": cells,
        "metadata": {"colab": {"provenance": []},
                     "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                     "language_info": {"name": "python"}},
        "nbformat": 4, "nbformat_minor": 0,
    }
    os.makedirs("notebooks", exist_ok=True)
    with open(f"notebooks/lesson{n}.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"notebooks/lesson{n}.ipynb: {len(cells)} cells")


if __name__ == "__main__":
    for n, lesson in LESSONS.items():
        build(n, lesson)
