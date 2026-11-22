# <Project name>: <one line on what it does for whom>

<One sentence on the result, with a number. Say if the client and data are simulated.>

![Demo](<link to a GIF or your demo video>)

## The problem

<Who the client is, what was going wrong, and the number that shows it. Two or three sentences.>

## What I built

<What it does, in plain words. Then a short list of the pieces.>

- <Piece 1>
- <Piece 2>
- <Piece 3>

## Results

| Metric | Before | After | How I measured it |
| --- | --- | --- | --- |
| <Your success metric> | <baseline> | <result> | <where the numbers came from> |
| <A second metric> | | | |

## How I know it works

- **Eval set:** <how many cases, what kinds, pass rate>
- **Guardrails:** <what they block>
- **What still fails:** <be honest: one or two known gaps>

## How to run it

```
<the commands to set it up and run it>
```

## What I'd do next

<One or two next steps, and why.>

---

<details>
<summary>Example: the Northstar admissions agent</summary>

# Northstar admissions agent: instant, accurate replies to WhatsApp enquiries

On a simulated skills institute with synthetic data, night enquiries went from a 10-hour wait to a reply
in seconds, with every fee answer checked against the current fee sheet.

## The problem

Northstar Skills (a fictional client) gets about 2,500 enquiries a month, 45% of them at night. Night enquiries
waited about 10 hours for a reply, and counsellors quoted fees from an out-of-date sheet.

## What I built

A WhatsApp agent that answers questions about courses, fees and campuses from Northstar's own documents,
books counselling calls, and hands sensitive chats to a counsellor with a short note.

- Retrieval over 12 course pages and policies, filtered to current documents only
- Tools for fees, free slots and safe booking (no double bookings, safe retries)
- Guardrails that block wrong fees, job promises and phone numbers
- Phone numbers and emails hidden before any model call

## Results

| Metric | Before | After | How I measured it |
| --- | --- | --- | --- |
| Median first reply to night enquiries | about 10 hours | about 7 seconds | Synthetic first-week log, 420 chats |
| Eval pass rate | — | 10 of 10 after fixes (8 of 10 at first) | 10 cases from real-style chats: 5 common, 3 tricky, 2 risky |

## How I know it works

- **Eval set:** 10 cases, with every risky case required to pass; failures from the first week added as tests
- **Guardrails:** block fees not in the sheet, job or refund promises, and phone numbers
- **What still fails:** an invented fact, like a hostel that doesn't exist, can get past simple guardrails;
  only the eval set and grounding catch it

## How to run it

```
git clone <your repo>
cd <your repo>/starter/northstar-agent
pip install google-genai anthropic openai sentence-transformers
```

## What I'd do next

A mentor helper that answers students' coding doubts from the course docs: the next pain the client named.

</details>
