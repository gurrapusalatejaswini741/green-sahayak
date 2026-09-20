"""
rag_chat.py
-----------
Combines retrieval (retrieval.py) with LLM generation to produce a
grounded, cited answer.
 
Two modes, chosen automatically based on whether GEMINI_API_KEY is set:
 
  1. LLM mode (if a Gemini API key is configured) - the retrieved chunks
     are given to Gemini as fixed context, and it's instructed to answer
     ONLY from that context, citing which source(s) it used, and to say
     so plainly if the context doesn't cover the question. This is the
     real RAG pipeline.
 
  2. Extractive fallback (no key configured) - returns the best-matching
     chunk directly, verbatim, with its source label. Less fluent, but
     100% functional with zero setup, so the app never breaks in a demo.
 
To enable LLM mode:
  1. Get a free API key at https://aistudio.google.com/apikey (Google AI Studio).
     As of mid-2026, Google issues "auth" keys (prefixed "AQ.") instead of the
     older "AIza..." keys - this module uses the current google-genai SDK,
     which supports both.
  2. pip install google-genai
  3. Set the environment variable GEMINI_API_KEY (never commit a real key to
     a public GitHub repo - use Streamlit Cloud's Secrets instead when deploying)
"""
 
import os
from retrieval import Retriever
 
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
 
SYSTEM_PROMPT = """You are GreenSahayak, a sustainability advisor for Indian households and
campuses. You will be given a user question and one or more CONTEXT passages retrieved from
a curated knowledge base. Rules:
1. Answer ONLY using information in the provided context. Do not use outside knowledge.
2. If the context does not contain enough information to answer, say so plainly rather than
   guessing.
3. Keep answers short and practical (3-5 sentences), in a warm but direct tone.
4. At the end, mention which topic(s) your answer drew from, e.g. "(Based on: E-Waste
   Disposal)".
5. Never fabricate a source or a fact not present in the context."""
 
 
def _build_context_block(retrieved: list) -> str:
    if not retrieved:
        return "No relevant context found."
    blocks = []
    for r in retrieved:
        blocks.append(f"[Source: {r['topic']}]\n{r['content']}")
    return "\n\n".join(blocks)
 
 
def _call_gemini(question: str, context_block: str) -> str:
    """
    Uses the current google-genai SDK and its Interactions API
    (client.interactions.create), which is what Google's docs recommend as
    of 2026 - the older google-generativeai package / GenerativeModel class
    is deprecated and doesn't work correctly with the newer "AQ." auth keys.
    """
    from google import genai
 
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f"CONTEXT:\n{context_block}\n\nUSER QUESTION: {question}"
 
    interaction = client.interactions.create(
        model="gemini-3-flash-preview",
        system_instruction=SYSTEM_PROMPT,
        input=prompt,
    )
    return interaction.output_text.strip()
 
 
def _extractive_fallback(question: str, retrieved: list) -> str:
    if not retrieved:
        return (
            "I don't have information on that in my current knowledge base. "
            "Try asking about waste segregation, e-waste, composting, water conservation, "
            "energy saving, plastic recycling, or battery disposal."
        )
    top = retrieved[0]
    return (
        f"{top['content']}\n\n"
        f"_(Based on: {top['topic']} \u2014 extractive mode, no LLM key configured)_"
    )
 
 
class GreenSahayak:
    def __init__(self):
        self.retriever = Retriever()
        self.llm_enabled = bool(GEMINI_API_KEY)
 
    def ask(self, question: str) -> dict:
        retrieved = self.retriever.retrieve(question, top_k=2)
 
        if self.llm_enabled:
            try:
                context_block = _build_context_block(retrieved)
                answer = _call_gemini(question, context_block)
                mode = "llm"
            except Exception as e:
                answer = _extractive_fallback(question, retrieved)
                mode = f"extractive (LLM call failed: {e})"
        else:
            answer = _extractive_fallback(question, retrieved)
            mode = "extractive (no API key configured)"
 
        return {
            "question": question,
            "answer": answer,
            "sources": [r["topic"] for r in retrieved],
            "retrieval_scores": [r["score"] for r in retrieved],
            "mode": mode,
        }
 
 
if __name__ == "__main__":
    bot = GreenSahayak()
    print(f"LLM enabled: {bot.llm_enabled}\n")
    for q in ["How do I dispose of an old phone battery?", "Can I compost eggshells?"]:
        result = bot.ask(q)
        print(f"Q: {result['question']}")
        print(f"A: {result['answer']}")
        print(f"Sources: {result['sources']} | Mode: {result['mode']}\n")
 
