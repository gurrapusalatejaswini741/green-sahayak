# GreenSahayak — RAG-based Civic Sustainability Advisor

**1M1B AI for Sustainability Virtual Internship** (with IBM SkillsBuild & AICTE)

## Problem Statement
> How might we use AI to answer citizens' waste-segregation and resource-conservation
> questions instantly and accurately, so that Indian households and campuses can adopt
> sustainable practices at scale?

**Primary SDG:** 12 — Responsible Consumption and Production
**Secondary:** SDG 11 — Sustainable Cities and Communities

This directly matches the internship's own suggested category: *"RAG system for
municipal waste policies."*

## How it works (RAG pipeline)
```
User question (text OR photo)
      │
      ├─ Text ─────────────────────────────────────────┐
      │                                                  ▼
      │                          retrieval.py — TF-IDF + cosine similarity
      │                          finds relevant entries in knowledge_base.py
      │
      └─ Photo (Snap & Sort) ────────────────────────────┐
                          vision_classify.py — Gemini Vision       │
                          identifies the item + a natural-language  │
                          query about disposing of it  ─────────────┘
                                          │
                                          ▼
                    rag_chat.py — retrieved chunks are given to an LLM
                    as FIXED context; the LLM is instructed to answer
                    ONLY from that context and cite which source it used
                                          │
                                          ▼
                    app.py — Streamlit UI (chat tab + Snap & Sort tab),
                    shows the answer + which knowledge base topic(s) it
                    was grounded in + retrieval confidence scores
```

**Snap & Sort** is the multimodal differentiator: photograph an item you're
unsure how to dispose of, and Gemini Vision identifies it and routes it
through the *same* grounded RAG pipeline as text questions — the vision
model never invents disposal advice on its own, it only identifies what
the item is.

**Why this is real RAG, not just an LLM wrapper:** the model is never allowed
to answer from its own general knowledge. If retrieval finds nothing relevant,
the system says so instead of guessing — this is the core Responsible AI
safeguard for this project (no hallucinated advice).

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Works immediately with **no API key** — it runs in extractive mode (returns
the best-matching knowledge base entry directly). This is enough for your
screenshots if you're short on time.

## Enable full LLM generation (recommended, ~5 minutes)
1. Go to https://ai.google.dev → "Get API key" → sign in with Google → create a
   free key (no credit card required)
2. Set it as an environment variable before running the app:
   - **Windows PowerShell:** `$env:GEMINI_API_KEY="your-key-here"`
   - **Mac/Linux:** `export GEMINI_API_KEY="your-key-here"`
3. Run `streamlit run app.py` again in the same terminal session
4. The sidebar should now show "LLM mode active (Gemini)" instead of the
   extractive-mode warning

**Never commit your API key to a public GitHub repo.** If deploying to
Streamlit Cloud, set it under the app's "Secrets" settings instead of in code.

## Deploy (free, for a shareable link)
1. Push this folder to a public GitHub repo (do NOT include your API key in any file)
2. Go to https://share.streamlit.io → "New app" → point it at the repo, main file `app.py`
3. In the app's Settings → Secrets, add: `GEMINI_API_KEY = "your-key-here"`
4. Deploy — you'll get a public URL for your submission

## Files
| File | Purpose |
|---|---|
| `knowledge_base.py` | Curated, original-wording sustainability guidance, organized by topic |
| `retrieval.py` | TF-IDF retrieval — finds relevant knowledge base entries for a query |
| `rag_chat.py` | Grounds LLM generation in retrieved context; extractive fallback if no key |
| `vision_classify.py` | Snap & Sort — Gemini Vision identifies a photographed item, feeds it into the RAG pipeline |
| `app.py` | Streamlit UI — text chat tab + Snap & Sort photo tab |

**Note:** Snap & Sort requires a Gemini API key (no offline fallback is honest for
real image recognition). If no key is set, that tab shows a clear message instead
of pretending to classify the image — text chat still works in extractive mode either way.

## Extending the knowledge base
Add more entries to `KNOWLEDGE_BASE` in `knowledge_base.py`, following the same
`{id, topic, source, content}` shape. More entries = broader question coverage
= a stronger demo. Good additions: local municipal rules for your specific
city, campus-specific waste rules, or seasonal water advisories.

## Responsible AI
- **Fairness** — knowledge base covers general household/campus practices, not tied to any specific community or demographic assumption
- **Transparency** — every answer names which knowledge base topic it was grounded in, and shows retrieval confidence scores
- **Ethics** — the system explicitly refuses to answer beyond its knowledge base rather than fabricating guidance
- **Privacy** — no personal data collected or stored; each question is processed independently with no user tracking
