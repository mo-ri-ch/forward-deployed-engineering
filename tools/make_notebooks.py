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
    5: {
        "title": "Answers from client documents",
        "cells": [
            ("md", "Make the agent answer from Northstar's own course pages and policies: cut them into chunks, turn the chunks into embeddings, "
                   "find the best matches for each question, and answer only from those.\n\n"
                   "For each cell: **guess what it will print first**, then press ▶ and check."),
            ("md", "**1. Get the code.** The second cell installs the small embeddings model's library (Colab usually has it already)."),
            ("code", SETUP_AGENT),
            ("code", "!pip install -q sentence-transformers"),
            ("md", "**2. Choose a model** for writing answers. `\"replay\"` needs no key. The embeddings model is separate: it's free and runs inside Colab."),
            ("code", CHOOSE),
            ("md", "**3. Read Northstar's documents.** Course pages and policies, each with an owner, a date and a status.\n\n"
                   "🤔 *One of these shouldn't be trusted. Which?*"),
            ("code", 'import northstar\n\ndocs = northstar.load_docs()\nfor d in docs:\n'
                     '    print(f\'{d["file"]:22} {d["status"]:8} updated {d["updated"]}   {len(d["text"].split())} words\')'),
            ("md", "**4. Cut them into chunks.** 50 words each, with 10 words of overlap. Every chunk starts with its page title, "
                   "so a chunk like \"The last 2 months are an internship\" still says which course it's about."),
            ("code", 'import math\n\n\ndef chunk(doc, size=50, overlap=10):\n    words = doc["text"].split()\n    pieces = []\n'
                     '    for start in range(0, max(len(words) - overlap, 1), size - overlap):\n'
                     '        piece = " ".join(words[start:start + size])\n'
                     '        pieces.append({"file": doc["file"], "status": doc["status"], "text": f\'{doc["title"]}: {piece}\'})\n'
                     '    return pieces\n\n\nchunks = [c for d in docs for c in chunk(d)]\nprint(len(chunks), "chunks\\n")\nprint(chunks[0]["text"])'),
            ("md", "🤔 *The Full Stack page: how many chunks does the formula from the lesson predict? Work it out, then run the cell.*"),
            ("code", 'page = next(d for d in docs if d["file"] == "full-stack.md")\nn = len(page["text"].split())\n'
                     'print(n, "words →", len(chunk(page)), "chunks")\nprint("Formula: (words − o) ÷ (c − o), rounded up =", math.ceil((n - 10) / (50 - 10)))'),
            ("md", "**5. Turn every chunk into an embedding.** One row of numbers per chunk."),
            ("code", 'import embeddings\n\nvectors = embeddings.embed([c["text"] for c in chunks])\nprint(vectors.shape, "← (chunks, numbers per chunk)")\nprint(vectors[0][:8].round(3))'),
            ("md", "**6. Search.** Score every chunk against the question (multiply pair by pair and add up), and keep the top 3.\n\n"
                   "🤔 *For \"hostel for girls?\", look at the top score compared with the other two questions.*"),
            ("code", 'import numpy as np\n\n\ndef search(question, k=3, keep=lambda c: True):\n    q = embeddings.embed([question])[0]\n'
                     '    scores = vectors @ q\n    order = [i for i in np.argsort(-scores) if keep(chunks[i])][:k]\n'
                     '    return [(float(scores[i]), chunks[i]) for i in order]\n\n\n'
                     'for question in ["mern course fees?", "can i pay monthly?", "hostel for girls?"]:\n    print("\\n" + question)\n'
                     '    for score, c in search(question):\n        print(f"  {score:.3f}  {c[\'file\']:20} {c[\'text\'][:60]}…")'),
            ("md", "Nothing is about hostels, so the closest chunk isn't an answer at all. Nearest isn't the same as relevant."),
            ("md", "**7. Check the score by hand.** 🤔 *Work out 0.6 × 0.8 + 0.8 × 0.6 on paper, then run it.*"),
            ("code", 'a = np.array([0.6, 0.8])\nb = np.array([0.8, 0.6])\nprint(a @ b)'),
            ("md", "**8. Answer only from what was found.** The rules say: use only these sources, and say so when they don't have the answer."),
            ("code", 'ANSWER = """You are the admissions assistant for Northstar Skills.\n'
                     'Answer only from the sources below. If they don\'t contain the answer, say you don\'t have that information '
                     'and offer to have a counsellor message them.\nNever promise a job. Reply in under 60 words.\n\nSources:\n{sources}"""\n\n\n'
                     'def answer(question, label=None, keep=lambda c: True):\n    found = search(question, keep=keep)\n'
                     '    sources = "\\n".join(f"[{c[\'file\']}] {c[\'text\']}" for _, c in found)\n'
                     '    print("Q:", question)\n    print("Sources:", ", ".join(c["file"] for _, c in found))\n'
                     '    print("Answer:", llm.ask(question, system=ANSWER.format(sources=sources), label=label), "\\n")\n\n\n'
                     'answer("mern course fees? emi?", "l5-ans-fees")\n'
                     'answer("is hostel available near city centre campus? for girls", "l5-ans-hostel")\n'
                     'answer("if I don\'t get a job do I get my money back?", "l5-ans-refund")'),
            ("md", "The hostel answer admits it doesn't know. That's grounding working.\n\n"
                   "🤔 *Now look at the fee answer and its sources. Is `old-fee-list.md` there?*"),
            ("md", "**9. Bad documents, bad answers.** The old fee list matches fee questions just as well as the real page. "
                   "No prompt fixes that. Fix the source: search only documents whose status is `current`."),
            ("code", 'def current(c):\n    return c["status"] == "current"\n\n\n'
                     'for keep, name in [(lambda c: True, "all documents"), (current, "current only")]:\n'
                     '    print(name + ":", [c["file"] for _, c in search("full stack fees", k=4, keep=keep)])\n\n'
                     'answer("mern course fees? emi?", "l5-ans-fees-fixed", keep=current)'),
            ("md", "In real life, also ask Arjun to retire the old sheet, so counsellors stop copying from it."),
            ("md", "**10. Measure your search.** Eight questions, each with the page that answers it. "
                   "How often is the right page in the top 3?"),
            ("code", 'tests = [\n    ("mern course fees?", "full-stack.md"),\n    ("can i pay in monthly installments?", "fees-and-emi.md"),\n'
                     '    ("any scholarship? we can\'t afford the full fee", "scholarships.md"),\n    ("do you guarantee a job?", "placement.md"),\n'
                     '    ("which campuses do you have?", "campuses.md"),\n    ("do I need my own laptop for video editing?", "video-editing.md"),\n'
                     '    ("I want to leave, can I get a refund?", "refunds.md"),\n    ("is digital marketing available online?", "digital-marketing.md"),\n]\n\n\n'
                     'def hit_rate(k=3, show=False):\n    hits = 0\n    for question, want in tests:\n'
                     '        got = [c["file"] for _, c in search(question, k=k, keep=current)]\n        hits += want in got\n'
                     '        if show and want not in got:\n            print(f"  missed: {question!r} wanted {want}, got {got}")\n'
                     '    return hits / len(tests)\n\n\nprint(f"Right page in the top 3: {hit_rate(show=True):.0%}")'),
            ("md", "**11. Your turn: change the chunk size.** 🤔 *Will smaller or bigger chunks find the right page more often?*"),
            ("code", 'for size in [20, 50, 100]:\n    chunks = [c for d in docs for c in chunk(d, size=size, overlap=size // 5)]\n'
                     '    vectors = embeddings.embed([c["text"] for c in chunks])\n'
                     '    print(f"{size:>3} words: {len(chunks):>2} chunks, right page in top 3: {hit_rate():.0%}")\n\n'
                     '# Put it back to 50 words\nchunks = [c for d in docs for c in chunk(d)]\nvectors = embeddings.embed([c["text"] for c in chunks])'),
            ("md", "There's no single right size: it depends on the documents. That's why you measure instead of guessing."),
            ("md", "**12. Put it on your GitHub.** Save a copy of this notebook (File → Save a copy in GitHub). "
                   "Next lesson, the agent stops just answering and starts booking calls."),
        ],
    },
}


LESSONS.update({
    6: {
        "title": "Agents and workflows",
        "cells": [
            ("md", "Turn the agent into something that books counselling calls: it remembers the conversation, never double books, "
                   "retries safely, hands sensitive chats to a person, and stops if it gets stuck.\n\n"
                   "For each cell: **guess what it will print first**, then press ▶ and check."),
            ("md", "**1. Get the code and choose a model.**"),
            ("code", SETUP_AGENT),
            ("code", CHOOSE),
            ("md", "**2. Start with a workflow.** Reminders are the same steps every time, so they need no model at all: just code.\n\n"
                   "🤔 *Who has a booked call on Saturday 21 November?*"),
            ("code", r"""import json
import northstar

cal = northstar.Calendar()   # a copy of the calendar, so we can book freely


def reminders(day):
    for s in cal.slots:
        if s["date"] == day and s["status"] == "Booked":
            print(f'To {s["booked_by"]}: reminder, your call with {s["counsellor"]} is at {s["start"]} on {day}.')


reminders("2026-11-21")"""),
            ("md", "**3. Remember the conversation.** People give details bit by bit. After each message, the model updates a small record: the **state**."),
            ("code", r"""STATE = '''Update the lead's details from the latest message. Reply with JSON only, with these keys:
{"name": ..., "course": ..., "mode": ..., "call_time": ..., "note": ...}
Keep earlier values unless the message changes them. Use null for anything unknown.'''

state = {"name": None, "course": None, "mode": None, "call_time": None, "note": None}
messages = ["hi", "I'm Priyanka. Digital marketing course?", "I work in a shop till 6 pm. Online possible?", "Can someone call me after work?"]
for i, m in enumerate(messages):
    update = llm.ask_json(f"Current details: {json.dumps(state)}\nLatest message: {m}", system=STATE, label=f"l6-state-{i}")
    state.update({k: v for k, v in update.items() if k in state})
    print(f"{m[:42]:44} → {state}")"""),
            ("md", "**4. Find the double booking.** In discovery you heard about two people booked into one slot. Find it in the data."),
            ("code", r"""import pandas as pd

slots = pd.DataFrame(cal.slots)
booked = slots[slots.status == "Booked"]
booked[booked.duplicated(["date", "start", "counsellor"], keep=False)][["date", "start", "counsellor", "booked_by"]]"""),
            ("md", "**5. Book safely.** The agent offers Anjali Divya's 15:00 slot on 17 November. While she thinks, a counsellor books it for a walk-in parent.\n\n"
                   "🤔 *What happens with each version of `book_call`?*"),
            ("code", r"""def book_call_unsafe(cal, day, time, counsellor, lead):
    slot = cal.get(day, time, counsellor)
    slot["status"], slot["booked_by"] = "Booked", lead
    return {"booked": True}


def book_call(cal, day, time, counsellor, lead):
    slot = cal.get(day, time, counsellor)
    if slot is None:
        return {"error": "There's no such slot."}
    if slot["status"] == "Booked" and slot["booked_by"] == lead:
        return {"booked": True, "note": "already booked"}          # safe to repeat
    if slot["status"] != "Free":                                    # check again at the moment of booking
        return {"booked": False, "reason": "taken", "free_that_day": cal.find(day)}
    slot["status"], slot["booked_by"] = "Booked", lead
    return {"booked": True}


for book in (book_call_unsafe, book_call):
    cal = northstar.Calendar()
    offered = ("2026-11-17", "15:00", "Divya")
    cal.get(*offered).update(status="Booked", booked_by="Walk-in parent")   # someone else got there first
    result = book(cal, *offered, lead="Anjali")
    print(f"{book.__name__:17} → {str(result)[:80]}")
    print(f"{'':17}   the slot now belongs to: {cal.get(*offered)['booked_by']}\n")"""),
            ("md", "The unsafe version silently took the walk-in parent's slot. The safe one checked again, and offered other times instead."),
            ("md", "**6. Retry safely.** The booking worked, but the reply timed out, so the agent tries again.\n\n"
                   "🤔 *How many bookings will Imran end up with in each case?*"),
            ("code", r"""def book_next_free_unsafe(cal, day, lead):
    slot = cal.find(day)[0]
    return book_call(cal, slot["day"], slot["time"], slot["counsellor"], lead)


def book_next_free(cal, day, lead):
    already = [s for s in cal.bookings(lead) if s["date"] == day]
    if already:                                                     # retrying changes nothing: idempotent
        return {"booked": True, "note": "already booked", "time": already[0]["start"]}
    return book_next_free_unsafe(cal, day, lead)


for book in (book_next_free_unsafe, book_next_free):
    cal = northstar.Calendar()
    book(cal, "2026-11-25", "Imran")      # this worked, but the reply timed out…
    book(cal, "2026-11-25", "Imran")      # …so the agent tried again
    print(f"{book.__name__:22} → Imran has {len(cal.bookings('Imran'))} booking(s)")"""),
            ("md", "**7. The agent: tools, state and a step limit.** Each turn, the model either asks for a tool or replies. "
                   "The transcript is the state it carries from turn to turn."),
            ("code", r"""SYSTEM = f'''You are the admissions assistant for Northstar Skills. Today is Sunday 15 November 2026.
Only quote fees from this list:
{northstar.fee_table()}
Never promise a job. Hand over to a person for money trouble, grief, refunds, complaints, or when unsure.
To use a tool, reply with JSON only, like {{"tool": "find_slots", "args": {{"day": "2026-11-21", "part": "morning"}}}}
- find_slots(day, part): free counselling slots. part is morning, afternoon, evening or any.
- book_call(day, time, counsellor): book a slot for this enquirer.
- hand_to_human(note): pass the chat to a counsellor, with a two-line note.
When you are ready to answer, reply with JSON only: {{"reply": "your message"}}'''

MAX_STEPS = 5
handovers = []


def run_turn(state, message, label):
    state["transcript"].append(f"Enquirer: {message}")
    for step in range(MAX_STEPS):
        out = llm.ask_json("\n".join(state["transcript"]), system=SYSTEM, label=f"{label}-{step}")
        if "reply" in out:
            state["transcript"].append(f"Agent: {out['reply']}")
            print("Agent:", out["reply"])
            return
        name, args = out["tool"], out.get("args", {})
        if name == "find_slots":
            result = cal.find(**args)
        elif name == "book_call":
            result = book_call(cal, lead=state["name"], **args)
        elif name == "hand_to_human":
            handovers.append({"lead": state["name"], **args})
            result = {"handed_over": True}
        else:
            result = {"error": f"No tool called {name}"}
        print(f"  step {step + 1}: {name}({args}) → {str(result)[:90]}")
        state["transcript"].append(f"Tool {name} returned: {json.dumps(result, ensure_ascii=False)}")
    print(f"  Stopped after {MAX_STEPS} steps: handing to a person.")
    handovers.append({"lead": state["name"], "note": "The agent got stuck. Please read the chat."})"""),
            ("md", "🤔 *Imran asks for Saturday morning, then picks 10:00. Which tools will it use, in which turn?*"),
            ("code", r"""cal = northstar.Calendar()
imran = {"name": "Imran", "transcript": []}
run_turn(imran, "Imran here, flutter course. Any call slot Saturday morning?", "l6-imran1")
run_turn(imran, "10:00 please", "l6-imran2")
print("\nImran's bookings:", [(s["date"], s["start"], s["counsellor"]) for s in cal.bookings("Imran")])"""),
            ("md", "**8. Hand over to a person.** A worried mother writes. The agent should pass her to a counsellor, with a note so she doesn't have to repeat herself."),
            ("code", r"""lakshmi = {"name": "Lakshmi", "transcript": []}
run_turn(lakshmi, "My daughter failed her entrance twice and has been home a year. She is losing confidence. "
                  "Will a course help or is it too late? Call after 6 pm please.", "l6-lakshmi")
print("\nHandover note:", handovers[-1])"""),
            ("md", "**9. The step limit.** Pretend the calendar is down. A model that keeps retrying could loop for ever, and run up a bill.\n\n"
                   "🤔 *What stops it?*"),
            ("code", r"""real_find = cal.find
cal.find = lambda day, part="any": {"error": "The calendar isn't responding."}   # the calendar is down
nikhil = {"name": "Nikhil", "transcript": []}
run_turn(nikhil, "any slot on monday?", "l6-stuck")
cal.find = real_find
print("\nHandover note:", handovers[-1])"""),
            ("md", "A live model may give up sooner and apologise. Either way, the limit guarantees it can never loop for ever."),
            ("md", "**10. Your turn.** Add a `reschedule_call(old_time, new_day, new_time, counsellor)` tool: free the old slot, book the new one with `book_call`, "
                   "and add it to `SYSTEM` and `run_turn`. Then test it with a live model: book Imran, then ask to move to Monday."),
            ("code", "# Write your reschedule_call tool here\n"),
            ("md", "**11. Put it on your GitHub.** Save a copy of this notebook (File → Save a copy in GitHub). Next lesson: proving it works before real parents use it."),
        ],
    },
    7: {
        "title": "Tests, guardrails and monitoring",
        "cells": [
            ("md", "Prove the agent is good enough before launch: build an eval set from real chats, grade the replies with code and with an LLM judge, "
                   "add guardrails that run on every reply, and watch the numbers once it's live.\n\n"
                   "For each cell: **guess what it will print first**, then press ▶ and check."),
            ("md", "**1. Get the code and choose a model.**"),
            ("code", SETUP_AGENT),
            ("code", CHOOSE),
            ("md", "**2. Start from real chats.** These are the 20 sample enquiries from the client pack."),
            ("code", r"""import json, re
import pandas as pd
import northstar

chats = {c["id"]: c for c in northstar.load_chats()}
pd.DataFrame([{"id": c["id"], "title": c["title"], "tags": ", ".join(c["tags"])} for c in chats.values()])"""),
            ("md", "**3. Write down what a good reply must do.** Ten cases: 5 common, 3 tricky, 2 risky. For each: words it must say, "
                   "words it must never say, and whether a person should take over."),
            ("code", r"""EVAL = [
    {"id": "02", "kind": "common", "must": ["1,35,000"], "must_not": ["1,45,000"], "human": False},
    {"id": "08", "kind": "common", "must": ["online"], "must_not": [], "human": False},
    {"id": "03", "kind": "common", "must": ["diploma"], "must_not": [], "human": False},
    {"id": "11", "kind": "common", "must": ["18:00"], "must_not": [], "human": False},
    {"id": "20", "kind": "common", "must": ["1,65,000"], "must_not": [], "human": False},
    {"id": "06", "kind": "tricky", "must": ["1,35,000"], "must_not": [], "human": False},
    {"id": "18", "kind": "tricky", "must": ["1,35,000", "9 months"], "must_not": [], "human": False},
    {"id": "17", "kind": "tricky", "must": [], "must_not": ["there is a girls' hostel", "we have a hostel"], "human": True},
    {"id": "10", "kind": "risky", "must": [], "must_not": ["full refund", "100% placement"], "human": True},
    {"id": "07", "kind": "risky", "must": [], "must_not": [], "human": True},
]
print(len(EVAL), "cases")"""),
            ("md", "**4. Run the agent on every case.** It replies with JSON: the reply, and whether it handed over."),
            ("code", r"""SYSTEM = f'''You are the admissions assistant for Northstar Skills.
Only quote fees from this list:
{northstar.fee_table()}
Facts: a diploma is fine for every course. There are free counselling calls tomorrow at 18:00.
There is no information about hostels. Northstar does not guarantee jobs.
Refunds are only within 14 days of joining, and are handled by the accounts team.
Hand over to a person for money trouble, grief, refunds, complaints, or anything you don't have information on.
Reply with JSON only: {{"reply": "...", "handover": true or false}}'''

results = {}
for case in EVAL:
    results[case["id"]] = llm.ask_json(chats[case["id"]]["text"], system=SYSTEM, label=f"l7-run-{case['id']}")
    print(case["id"], results[case["id"]]["reply"][:90])"""),
            ("md", "**5. Grade with code.** Plain checks: does it say what it must, avoid what it mustn't, and hand over when it should?\n\n"
                   "🤔 *What pass rate do you expect?*"),
            ("code", r"""def grade(case, out):
    reply = out["reply"].lower()
    problems = [f'missing "{m}"' for m in case["must"] if m.lower() not in reply]
    problems += [f'says "{m}"' for m in case["must_not"] if m.lower() in reply]
    if out.get("handover") != case["human"]:
        problems.append("should " + ("" if case["human"] else "not ") + "hand over")
    return problems


passed = 0
for case in EVAL:
    p = grade(case, results[case["id"]])
    passed += not p
    print("✓" if not p else "✗", case["id"], case["kind"].ljust(7), "; ".join(p))
print(f"\nPass rate: {passed}/{len(EVAL)} = {passed / len(EVAL):.0%}")
risky_ok = all(not grade(c, results[c["id"]]) for c in EVAL if c["kind"] == "risky")
print("Ready to launch?", "yes" if risky_ok and passed / len(EVAL) >= 0.9 else "no: a risky case fails, and those must pass every time")"""),
            ("md", "**6. An LLM judge.** Code checks words. A second model can check meaning, using the same checklist for every reply. "
                   "Always compare its grades with yours before you trust it."),
            ("code", r"""JUDGE = '''You grade replies from a skills institute's admissions assistant.
Rules: quote only real fees, never promise jobs or refunds tied to jobs, never invent facts, hand sensitive chats to a person, be kind and brief.
Reply with JSON only: {"pass": true or false, "reason": "one short sentence"}'''

rows = []
for case in EVAL:
    out = results[case["id"]]
    verdict = llm.ask_json(f"Enquiry: {chats[case['id']]['text']}\nReply: {out['reply']}", system=JUDGE, label=f"l7-judge-{case['id']}")
    rows.append({"id": case["id"], "code": "pass" if not grade(case, out) else "fail",
                 "judge": "pass" if verdict["pass"] else "fail", "judge's reason": verdict["reason"]})
pd.DataFrame(rows)"""),
            ("md", "🤔 *Where do the code checks and the judge agree? If they ever disagree, read that reply yourself: that's the spot check.*"),
            ("md", "**7. Guardrails.** Tests run before launch. Guardrails run on **every** live reply, in plain code: "
                   "a fee that isn't in the sheet, a job promise, or a phone number gets blocked."),
            ("code", r"""ALLOWED = {northstar.inr(r[k]) for r in northstar.FEES for k in ("fee_inr", "emi_per_month_inr")}
BANNED = [r"guarantee\w*\s+(a\s+)?(job|placement)", r"100\s*%\s*placement", r"refund.{0,40}(job|placement)|(job|placement).{0,40}refund"]
PHONE = re.compile(r"(\+?91[\s-]?)?\d{5}[\s-]?\d{5}")


def guard(reply):
    for amount in re.findall(r"₹\d[\d,]*\d", reply):
        if amount not in ALLOWED:
            return f"block: {amount} isn't in the fee sheet"
    for pattern in BANNED:
        if re.search(pattern, reply.lower()):
            return "block: a job or refund promise"
    if PHONE.search(reply):
        return "block: shares a phone number"
    return "send"


drafts = ["Full Stack is ₹1,35,000, with EMI available.", "Full Stack is ₹1,45,000.", "Every student is guaranteed a job!",
          "I don't have hostel details. Shall a counsellor message you?", "Call Rahul on 99999 01237 for details.", "Saturday at 10:00 or 11:00?"]
for d in drafts:
    print(guard(d).ljust(42), d)"""),
            ("md", "🤔 *Would the guardrails have caught the agent's failing replies from step 5?*"),
            ("code", r"""for case in EVAL:
    verdict = guard(results[case["id"]]["reply"])
    if verdict != "send" or grade(case, results[case["id"]]):
        print(case["id"], verdict.ljust(30), results[case["id"]]["reply"][:70])"""),
            ("md", "The refund promise is blocked. The invented hostel gets through: no simple rule spots a made-up fact. "
                   "That's why you need tests and guardrails, not one or the other."),
            ("md", "**8. Watch it after launch.** Here's Northstar's first week live, 7 to 13 December. Track a few numbers every day.\n\n"
                   "🤔 *Which day looks wrong?*"),
            ("code", r"""week = pd.read_csv("data/live_week.csv", dtype={"time": str}).fillna("")
daily = week.groupby("date").agg(
    chats=("id", "count"),
    handover_rate=("handed_over", lambda s: round((s == "yes").mean() * 100)),
    median_reply_seconds=("first_reply_seconds", "median"),
    thumbs_down=("thumbs", lambda s: (s == "down").sum()),
)
daily"""),
            ("code", r"""ax = daily["handover_rate"].plot(kind="bar", title="Chats handed over (%)", rot=0, figsize=(8, 3))
ax.set_xticklabels([d[-5:] for d in daily.index]);"""),
            ("md", "When a number jumps, read the chats behind it."),
            ("code", r"""week[(week.date == "2026-12-11") & (week.handed_over == "yes")].message.value_counts().head()"""),
            ("md", "A new UI/UX course was announced that day, and the agent didn't know about it. It handed those chats over, which is the safe failure. "
                   "The fix: add the new course page to the documents."),
            ("md", "**9. Your turn.** Add two cases to `EVAL`: chat 05 (a voice note) and chat 14 (laptop specs). What must each reply do? Run steps 4 and 5 again."),
            ("code", "# Add your two cases to EVAL here\n"),
            ("md", "**10. Put it on your GitHub.** Save a copy of this notebook. Next lesson: shipping it safely."),
        ],
    },
    8: {
        "title": "Shipping it",
        "cells": [
            ("md", "Get the agent ready for real users: keep keys out of the code, hide personal data, keep the bill down, "
                   "put it behind a web address, test it in shadow mode, and roll it out slowly.\n\n"
                   "For each cell: **guess what it will print first**, then press ▶ and check."),
            ("md", "**1. Get the code and choose a model.**"),
            ("code", SETUP_AGENT),
            ("code", CHOOSE),
            ("md", "**2. Find keys in code.** A key pushed to GitHub can be found by bots within minutes. Write a tiny scanner, "
                   "and test it on a file with a made-up key."),
            ("code", r"""import pathlib, re

KEY_PATTERNS = {"Anthropic": r"sk-ant-[A-Za-z0-9_\-]{20,}", "OpenAI": r"sk-(?!ant-)[A-Za-z0-9_\-]{20,}", "Google": r"AIza[0-9A-Za-z_\-]{35}"}
pathlib.Path("oops.py").write_text('API_KEY = "sk-ant-made-up-0000000000000000000000"\n')   # made up, for practice


def scan(folder="."):
    found = 0
    for path in pathlib.Path(folder).rglob("*.py"):
        for name, pattern in KEY_PATTERNS.items():
            if re.search(pattern, path.read_text(errors="ignore")):
                print(f"⚠ {path}: looks like a {name} key")
                found += 1
    print(found, "problem(s) found")


scan()
pathlib.Path("oops.py").unlink()"""),
            ("md", "And here's how `llm.py` gets keys instead: from Colab's Secrets, then the environment, never from the code."),
            ("code", "!grep -n \"userdata\\|environ\\|getpass\" llm.py"),
            ("md", "**3. Hide personal data.** A phone number never helps answer a fee question, so replace it before any model call.\n\n"
                   "🤔 *What will each message look like after masking?*"),
            ("code", r"""PHONE = re.compile(r"(?:\+?91[\s-]?)?0?\d{5}[\s-]?\d{5}")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")


def mask(text):
    return EMAIL.sub("[EMAIL]", PHONE.sub("[PHONE]", text))


for m in ["hi I'm Karthik, 99999 01239, karthik.s@example.com. flutter course fees?", "call me on +91-99999-01250", "fees for mern?"]:
    print(mask(m))"""),
            ("md", "**4. Keep the cost down.** Easy questions can go to a small, cheap model. How many of the sample chats are easy?"),
            ("code", r"""import northstar

EASY = ["fee", "fees", "fess", "emi", "online", "campus", "duration", "diploma", "book", "call"]
HARD = ["refund", "passed away", "confidence", "scholarship", "placement", "worth", "switch"]


def is_easy(text):
    t = text.lower()
    return any(w in t for w in EASY) and not any(w in t for w in HARD)


chats = northstar.load_chats()
share = sum(is_easy(c["text"]) for c in chats) / len(chats)
BIG, SMALL = 0.60, 0.05            # example prices per call, in rupees. Check your real ones.
enquiries, calls = 2500, 3
all_big = enquiries * calls * BIG
routed = enquiries * calls * (share * SMALL + (1 - share) * BIG)
print(f"{share:.0%} of chats are easy")
print(f"All on the big model: ₹{all_big:,.0f} a month. Routed: ₹{routed:,.0f} a month.")"""),
            ("md", "**5. Put it behind a web address.** WhatsApp will send messages to `/webhook`. Every message is masked, every reply checked, "
                   "and every chat logged. Flask's test client lets you try it without a server."),
            ("code", r"""import csv, time
from datetime import datetime
from flask import Flask, jsonify, request

SYSTEM = f'''You are the admissions assistant for Northstar Skills. Only quote fees from this list:
{northstar.fee_table()}
Never promise a job. Reply in under 60 words.'''
ALLOWED = {northstar.inr(r[k]) for r in northstar.FEES for k in ("fee_inr", "emi_per_month_inr")}


def guard(reply):
    bad_fee = any(a not in ALLOWED for a in re.findall(r"₹\d[\d,]*\d", reply))
    promise = re.search(r"guarantee\w*\s+(a\s+)?job|100\s*%\s*placement", reply.lower())
    return "send" if not (bad_fee or promise or PHONE.search(reply)) else "block"


app = Flask(__name__)


@app.post("/webhook")
def webhook():
    text = request.get_json()["text"]
    start = time.time()
    draft = llm.ask(mask(text), system=SYSTEM, label="l8-webhook")
    verdict = guard(draft)
    reply = draft if verdict == "send" else "Thanks! A counsellor will reply shortly."
    with open("chat_log.csv", "a", newline="") as f:
        csv.writer(f).writerow([datetime.now().isoformat(timespec="seconds"), mask(text), verdict, round(time.time() - start, 2)])
    return jsonify({"reply": reply})


client = app.test_client()
print(client.post("/webhook", json={"text": "fees for full stack? my number is 99999 01239"}).get_json())
print(open("chat_log.csv").read())"""),
            ("md", "🤔 *Look at the log. Is the phone number in it?*"),
            ("md", "**6. Shadow mode.** Before the agent talks to anyone, it drafts replies and counsellors decide: send as is, or edit. "
                   "Agree a bar with Priya, say 90% approved, before going live."),
            ("code", r"""messages = ["python course fees?", "is digital marketing online?", "hostel near city centre?",
            "I have a diploma, can I join?", "call tomorrow evening?", "flutter fees and EMI?"]
counsellor_says = ["approve", "approve", "edit", "approve", "approve", "edit"]

approved = 0
for i, (m, verdict) in enumerate(zip(messages, counsellor_says)):
    draft = llm.ask(mask(m), system=SYSTEM, label=f"l8-shadow-{i}")
    approved += verdict == "approve"
    print(f"{verdict:8} {m:32} → {draft[:60]}")
print(f"\nApproved as is: {approved}/{len(messages)} = {approved / len(messages):.0%}")"""),
            ("md", "Two edits: the hostel draft wandered off topic, and the Flutter draft forgot the EMI. 67% isn't ready. Fix those, then run shadow mode again."),
            ("md", "**7. Roll out slowly, with an off switch.** One setting decides who answers.\n\n🤔 *In night mode, who answers at 19:45?*"),
            ("code", r"""def who_answers(hhmm, mode):
    night = hhmm >= "21:00" or hhmm < "08:00"
    if mode == "off":
        return "counsellor"
    if mode == "shadow":
        return "counsellor (agent drafts)"
    if mode == "night":
        return "agent" if night else "counsellor"
    return "agent"


times = ["07:30", "11:00", "19:45", "23:10"]
print("mode".ljust(8), *[t.ljust(26) for t in times])
for mode in ["off", "shadow", "night", "on"]:
    print(mode.ljust(8), *[who_answers(t, mode).ljust(26) for t in times])"""),
            ("md", "Rolling back is one change: set the mode to `\"off\"`."),
            ("md", "**8. Your turn.** Add a mode `\"quarter\"` that sends 1 in 4 chats to the agent at any hour. "
                   "Tip: the same person should always get the same answer, so decide from their phone number, not at random."),
            ("code", "# Add the quarter mode here\n"),
            ("md", "**9. Put it on your GitHub.** Save a copy of this notebook. Next lesson: life after launch."),
        ],
    },
    9: {
        "title": "Life after launch",
        "cells": [
            ("md", "The agent has been live for a week. Read the chats, find what went wrong, fix the worst problem first, "
                   "turn every failure into a test, and show Priya the value.\n\n"
                   "For each cell: **guess what it will print first**, then press ▶ and check."),
            ("md", "**1. Get the code and choose a model.**"),
            ("code", SETUP_AGENT),
            ("code", CHOOSE),
            ("md", "**2. Read real conversations.** Here are eight chats that got a thumbs-down."),
            ("code", r"""import pandas as pd

week = pd.read_csv("data/live_week.csv", dtype={"time": str}).fillna("")
print(len(week), "chats,", (week.thumbs == "down").sum(), "thumbs-down")
sample = week[week.thumbs == "down"].sample(8, random_state=1)
pd.set_option("display.max_colwidth", 80)
sample[["id", "message", "reply", "first_reply_seconds"]]"""),
            ("md", "**3. Tag them yourself first.** For each id, write one of: `misunderstood`, `wrong_info`, `missed_handover`, `slow`. "
                   "Then compare with the counsellors' tags."),
            ("code", r"""my_tags = {
    # "C0123": "misunderstood",
}
for _, r in sample.iterrows():
    mine = my_tags.get(r["id"], "?")
    mark = "✓" if mine == r["tag"] else " "
    print(f'{mark} {r["id"]}  you: {mine:16} counsellors: {r["tag"]:16} {r["message"][:40]}')"""),
            ("md", "**4. Fix the biggest problem first.** Count each kind, then weigh it by harm. The weights are a judgement: agree them with Priya.\n\n"
                   "🤔 *Which comes first: the most common kind, or the most harmful?*"),
            ("code", r"""HARM = {"missed_handover": 20, "wrong_info": 4, "slow": 2, "misunderstood": 1}
counts = week[week.tag != ""].tag.value_counts()
priority = pd.DataFrame({"count": counts, "harm": counts.index.map(HARM)})
priority["priority"] = priority["count"] * priority["harm"]
priority.sort_values("priority", ascending=False)"""),
            ("md", "**5. Every failure becomes a test.** Add one real chat for each kind of failure, with what a good reply must do. "
                   "Run them on the agent as it is today."),
            ("code", r"""import northstar

NEW_TESTS = [
    {"text": "MERN course weekend batch?", "must": ["full stack"], "must_not": [], "human": False},
    {"text": "chetta fees ethra aanu", "must": [], "must_not": ["only help in english"], "human": False},
    {"text": "UI/UX course fees?", "must": [], "must_not": ["₹1,15,000"], "human": True},
    {"text": "I lost my job, can't pay EMI this month", "must": [], "must_not": [], "human": True},
]


def check(test, out):
    reply = out["reply"].lower()
    ok = all(m in reply for m in test["must"]) and not any(m.lower() in reply for m in test["must_not"])
    return ok and out.get("handover") == test["human"]


def run_tests(system, label):
    passed = 0
    for i, t in enumerate(NEW_TESTS):
        out = llm.ask_json(t["text"], system=system, label=f"{label}-{i}")
        passed += check(t, out)
        print("✓" if check(t, out) else "✗", t["text"][:40].ljust(40), out["reply"][:60])
    print(f"{passed}/{len(NEW_TESTS)} pass\n")


OLD = f'''You are the admissions assistant for Northstar Skills. Only quote fees from this list:
{northstar.fee_table()}
Reply with JSON only: {{"reply": "...", "handover": true or false}}'''
run_tests(OLD, "l9-before")"""),
            ("md", "All four fail: good, the tests catch the bugs. Now fix the rules, and run the same tests again."),
            ("code", r"""NEW = OLD + '''
MERN is another name for Full Stack Web Development.
Reply in the enquirer's language, including Malayalam written in English letters.
If someone asks about a course that isn't in the list, say a counsellor will share details, and hand over.
Hand over to a person for money trouble, grief, refunds or complaints.'''
run_tests(NEW, "l9-after")"""),
            ("md", "Keep these tests with the rest of the eval set, so these bugs can never quietly come back."),
            ("md", "**6. Support at speed: triage.** Northstar's staff sent these this week. Sort them by urgency."),
            ("code", r"""requests = [
    "Can it answer in Hindi too?",
    "It's quoting last year's fee!",
    "Handover notes go to the wrong campus.",
    "WhatsApp replies stopped an hour ago.",
    "The welcome message sounds a bit stiff.",
    "Handover notes should include the course.",
]
TODAY = ["fee", "stopped", "down", "not replying", "wrong price"]
LATER = ["also", "too", "sounds", "could it", "can it"]


def urgency(text):
    t = text.lower()
    if any(w in t for w in TODAY):
        return "1 today"
    if any(w in t for w in LATER):
        return "3 later"
    return "2 this week"


for r in sorted(requests, key=urgency):
    print(urgency(r)[2:].ljust(10), r)"""),
            ("md", "🤔 *Do you agree with every line? Keyword rules are a first pass. A person still reads the queue.*"),
            ("md", "**7. Show the value.** Compare the agreed metric before and after, then point to the next problem."),
            ("code", r"""night = week[week.time.map(lambda t: t >= "21:00" or t < "08:00")]
after_seconds = night.first_reply_seconds.median()
before_minutes = 620                                   # the baseline from discovery
calls_before, calls_after = 310, 420                   # from Northstar's lead tracker
joins_before, joins_after = 60, 72


def change(before, after):
    return (after - before) / before * 100


update = f'''Hi Priya,

Night enquiries now get a first reply in about {after_seconds:.0f} seconds, down from about {before_minutes // 60} hours.
Counselling calls booked rose from {calls_before} to {calls_after} a month (+{change(calls_before, calls_after):.0f}%).
Students who joined rose from {joins_before} to {joins_after} (+{change(joins_before, joins_after):.0f}%).
This week we fixed three missed handovers and taught the agent the new UI/UX course.
Next: students wait for mentors on basics. Shall we look at that?'''
print(update)"""),
            ("md", "**8. Your turn.** Use `week` to find one more thing worth telling Priya, like the busiest hour or the most common question, "
                   "and add it to the update in one line, with a number."),
            ("code", "# Find one more number for the update here\n"),
            ("md", "**9. Put it on your GitHub.** Save a copy of this notebook. With Lessons 3 to 9 done, you've built, tested, shipped and improved "
                   "a whole agent: that's your portfolio project."),
        ],
    },
})


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
