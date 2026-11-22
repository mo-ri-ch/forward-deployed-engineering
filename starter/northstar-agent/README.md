# northstar-agent

The admissions agent you build in the [Forward Deployed Engineering](https://gradlabs.in/learn/fde/) course,
one notebook at a time. Northstar Skills is a fictional client: every name, fee and message here is made up.

| File | What it is |
| --- | --- |
| `llm.py` | One `ask()` helper for Gemini, Claude or OpenAI, plus a no-key replay mode |
| `recorded.py` | The recorded answers replay mode uses |
| `northstar.py` | Northstar's data and tools: `get_fee`, `find_slots`, `Calendar`, `load_docs`, `load_chats` |
| `embeddings.py` | Free embeddings that run in Colab (all-MiniLM-L6-v2), with an offline fallback |
| `data/fees.csv` | The current fee sheet |
| `data/slots.csv` | Counselling slots, 16 to 28 November |
| `data/docs/` | Course pages and policies, plus one out-of-date fee list |
| `data/sample_chats.json` | The 20 sample enquiries from the client pack |
| `data/live_week.csv` | The agent's first week live, 7 to 13 December, with tagged failures |

## Choosing a model

```python
import llm
llm.setup("gemini")   # free tier: make a key at aistudio.google.com
llm.setup("claude")   # your Anthropic key
llm.setup("openai")   # your OpenAI key
llm.setup("replay")   # no key: recorded answers, so every notebook still runs
```

In Colab, save your key under 🔑 Secrets (for example `GEMINI_API_KEY`) and `setup` finds it.
Free tiers may use what you send to improve the provider's products. That's fine for this made-up data,
but never send a real client's data to a free tier.
