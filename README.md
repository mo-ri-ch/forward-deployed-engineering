# Forward Deployed Engineering

Learn the forward deployed engineer's job by doing it: take one client from a vague brief to a working
AI system, then look after it once it's live.

**Read it here:** [gradlabs.in/learn/fde](https://gradlabs.in/learn/fde/)

| Lesson | What it covers |
| --- | --- |
| 1. Meet your client | What an FDE does, and the client you'll work with all course |
| 2. Discovery | Turn a vague brief into one clear problem, with a number to prove it's solved |
| 3. Reading someone else's code | Find your way around a client's codebase, and fix a bug safely |
| 4. Building with LLMs | Prompts, answers in a fixed shape, and tools |
| 5. Answers from client documents | Retrieval (RAG): chunks, embeddings, grounding |
| 6. Agents and workflows | Booking a call step by step, handovers, safe retries |
| 7. Tests, guardrails and monitoring | Eval sets, grading, guardrails, watching it live |
| 8. Shipping it | Keys, personal data, cost and a slow rollout |
| 9. Life after launch | Reading real chats, fixing what matters, showing value |
| 10. Talking to the client | Updates, demos, bad news and scope creep |
| 11. Capstone | Run your own engagement for your portfolio |
| 12. Interview practice | Cases, system design, role-play and your project story |

## Build it yourself

Hands-on Colab notebooks build the Northstar admissions agent step by step, on real starter code and data:

| Notebook | What you do |
| --- | --- |
| [Lesson 3](notebooks/lesson3.ipynb) | Fix the duplicate-lead bug in Kevin's code, with tests, and clean up the sheet |
| [Lesson 4](notebooks/lesson4.ipynb) | Call a real model: system prompt, JSON answers, a tiny eval set, and tools for fees and slots |
| [Lesson 5](notebooks/lesson5.ipynb) | Chunk Northstar's documents, embed and search them, answer only from sources, catch the old fee list, measure search |
| [Lesson 6](notebooks/lesson6.ipynb) | State, safe bookings and retries, handovers with notes, a step limit |
| [Lesson 7](notebooks/lesson7.ipynb) | An eval set from real chats, code checks and an LLM judge, guardrails, monitoring the first week |
| [Lesson 8](notebooks/lesson8.ipynb) | Key scanning, masking personal data, routing to cut cost, a logged webhook, shadow mode, rollout modes |
| [Lesson 9](notebooks/lesson9.ipynb) | Tag a week of failures, fix the worst first, turn failures into tests, triage, the monthly update |

For interviews: ten [interview cases](https://gradlabs.in/learn/fde/lessons/cases.html) with what a strong answer covers, and [coding round practice](notebooks/coding-round.ipynb), eight timed exercises with checks ([model answers](notebooks/coding-round-solutions.ipynb)).

To apply with it: [portfolio templates](portfolio/) for your README, demo video, write-up, resume and LinkedIn.

Starter code lives in [`starter/`](starter/). The notebooks are built from `tools/make_notebooks.py`; the first-week log from `tools/make_live_week.py`.

The client, Northstar Skills, is made up. Every name, number and message in the course is invented.

Built with the shared [study notebook design](https://github.com/mo-ri-ch/study-notebook-design).
