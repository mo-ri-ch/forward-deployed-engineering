# <Project name>

*<One line: client (say if simulated), what you built, the result.>*

## The problem

<Two or three sentences. Who, what went wrong, the number.>

## What I found in discovery

<Two or three findings from interviews and data that changed the plan. Include one thing that surprised you.>

## What I built, and why

<The first version, and the choices behind it. Why this, and not something bigger?>

## How I proved it works

<Eval set, guardrails, the pass rate, and what still fails.>

## The result

<Before and after, with how you measured it.>

## What I learned

<One or two honest lessons. A mistake you made and fixed is worth more than a perfect story.>

---

<details>
<summary>Example: the Northstar admissions agent</summary>

# Northstar admissions agent

*A WhatsApp admissions agent for a simulated skills institute, built on synthetic data. Night enquiries went from
a 10-hour wait to a reply in seconds.*

## The problem

Northstar Skills gets about 2,500 enquiries a month. Its director said things felt chaotic, but the brief had no
numbers. Discovery showed the real problem: 45% of enquiries arrive at night and waited about 10 hours, so leads went cold.

## What I found in discovery

Admissions was judged on calls booked, while the director cared about students who join: different goals. Two fee
sheets disagreed, so counsellors quoted old fees. And the IT lead's worry about phone numbers turned out to be the
biggest risk to the project, so I planned around it from day one.

## What I built, and why

Only the admissions agent, out of four options I scored, because it had the most value and the most ready data.
It answers from Northstar's documents, books calls with tools, and hands sensitive chats to a person. I left out
mentoring and job matching on purpose, and said so in the scope doc.

## How I proved it works

A 10-case eval set from real-style chats, with code checks and an LLM judge. The first run passed 8 of 10: it
invented a hostel and promised a refund. Guardrails caught the refund promise but not the hostel, which taught me
that guardrails and tests do different jobs. After fixes, all 10 passed.

## The result

On a synthetic first week of 420 chats, the median night reply was about 7 seconds, down from about 10 hours.

## What I learned

The data was harder than the model: removing the old fee sheet from the search fixed more than any prompt change.
And the rarest failure, three missed handovers, mattered most.

</details>
