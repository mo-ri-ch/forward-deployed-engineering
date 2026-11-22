# Demo video script (about 3 minutes)

Most people who look at your project watch this and nothing else. Same shape as a client demo:
the problem, their data, it working, the number, what's next. Record your screen, talk over it, and cut the pauses.

| Time | What to show | What to say |
| --- | --- | --- |
| 0:00–0:20 | A slide or the chat app | The problem, in the client's words, with one number. |
| 0:20–0:40 | The messy data | What you found in it that mattered. |
| 0:40–2:10 | It working, on a real case | One normal case, then one tricky case it handles safely. |
| 2:10–2:30 | The number | Before and after, and how you measured it. |
| 2:30–3:00 | What's next | One next step, and what you learned. |

## Your script

**0:00 The problem.** "<client> was <problem>. <number>."

**0:20 The data.** "<what you found in their data>."

**0:40 It working.** "Here's a <normal case>. <what happens>. Now a harder one: <tricky case>. <how it handles it safely>."

**2:10 The number.** "<metric> went from <before> to <after>, measured on <how>."

**2:30 Next.** "Next I'd <next step>. The biggest lesson: <lesson>."

---

<details>
<summary>Example: the Northstar admissions agent</summary>

**0:00 The problem.** "Northstar Skills, a fictional skills institute, gets 2,500 enquiries a month. Almost half
arrive at night, and they waited about 10 hours for a reply. By morning, the lead had gone cold."

**0:20 The data.** "Their data was messy: two fee sheets that disagreed, the same person saved three times
under different phone formats, and messages in English mixed with Malayalam."

**0:40 It working.** "Here's a parent at 11 pm: 'wat is fees for python course, emi possible?' It finds the
current fee, replies in seconds, and offers a call on Saturday, checking the slot is still free before booking.
Now a harder one: a mother whose daughter failed her entrance exams twice. The agent doesn't try to sell. It hands
her to a counsellor, with a two-line note so she doesn't have to repeat herself."

**2:10 The number.** "On a synthetic first week of 420 chats, the median night reply went from about 10 hours to
about 7 seconds. It passes all 10 test cases, including the two risky ones."

**2:30 Next.** "Next I'd build a helper for students' coding doubts. The biggest lesson: the data was harder than the
model. Fixing the fee sheet mattered more than any prompt."

</details>
