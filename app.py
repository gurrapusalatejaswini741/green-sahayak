"""
GreenSahayak - RAG-based Civic Sustainability Advisor
1M1B AI for Sustainability Virtual Internship (with IBM SkillsBuild & AICTE)

Run locally:    streamlit run app.py
"""

import streamlit as st
from PIL import Image

from rag_chat import GreenSahayak
from knowledge_base import KNOWLEDGE_BASE

st.set_page_config(page_title="GreenSahayak", page_icon="\U0001F331", layout="wide")

if "bot" not in st.session_state:
    st.session_state.bot = GreenSahayak()
if "history" not in st.session_state:
    st.session_state.history = []

bot = st.session_state.bot

st.title("\U0001F331 GreenSahayak")
st.caption("A RAG-based sustainability advisor \u2014 built for the 1M1B AI for Sustainability Virtual Internship")

with st.sidebar:
    st.header("About this project")
    st.markdown(
        "**SDG 12** \u2014 Responsible Consumption & Production (primary)\n\n"
        "**SDG 11** \u2014 Sustainable Cities and Communities (secondary)\n\n"
        "This is a **Retrieval-Augmented Generation (RAG)** system: every "
        "answer is grounded in a curated knowledge base, not the model's "
        "general knowledge. If the knowledge base doesn't cover a "
        "question, the app says so instead of guessing.\n\n"
        "**Snap & Sort** adds a multimodal layer: photograph an item, and "
        "the same RAG pipeline grounds the disposal guidance for it."
    )
    st.divider()
    st.subheader("Knowledge base topics")
    for entry in KNOWLEDGE_BASE:
        st.markdown(f"- {entry['topic']}")
    st.divider()
    if bot.llm_enabled:
        st.success("LLM mode active (Gemini)")
    else:
        st.warning("Running in extractive mode \u2014 set GEMINI_API_KEY for full LLM generation and to enable Snap & Sort")

tab_chat, tab_snap = st.tabs(["\U0001F4AC Ask a Question", "\U0001F4F7 Snap & Sort"])

# ---------------------------------------------------------------------
with tab_chat:
    st.subheader("Ask a question")
    example_cols = st.columns(3)
    examples = [
        "How do I dispose of an old phone battery?",
        "Can I compost eggshells?",
        "How can I reduce my water usage at home?",
    ]
    clicked_example = None
    for col, ex in zip(example_cols, examples):
        if col.button(ex, use_container_width=True):
            clicked_example = ex

    question = st.chat_input("Ask about waste, water, energy, or recycling...")
    final_question = clicked_example or question

    if final_question:
        st.session_state.history.append(final_question)
        result = bot.ask(final_question)
        st.session_state.history[-1] = result

    for item in st.session_state.history:
        if isinstance(item, dict):
            with st.chat_message("user"):
                st.write(item["question"])
            with st.chat_message("assistant"):
                st.write(item["answer"])
                if item["sources"]:
                    st.caption(
                        f"Retrieved from: {', '.join(item['sources'])} "
                        f"(similarity: {', '.join(str(s) for s in item['retrieval_scores'])}) "
                        f"\u00b7 mode: {item['mode']}"
                    )

# ---------------------------------------------------------------------
with tab_snap:
    st.subheader("Snap & Sort")
    st.write(
        "Upload or take a photo of an item you're unsure how to dispose of. "
        "Gemini Vision identifies it, and the same knowledge base grounds the guidance."
    )

    if not bot.llm_enabled:
        st.warning(
            "Snap & Sort needs a Gemini API key to understand images \u2014 there's no "
            "honest offline fallback for real image recognition. Set GEMINI_API_KEY "
            "(see README) to enable this tab."
        )
    else:
        uploaded = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"])
        camera_photo = st.camera_input("...or take a photo")
        image_file = uploaded or camera_photo

        if image_file:
            image = Image.open(image_file)
            col_img, col_result = st.columns([1, 2])
            with col_img:
                st.image(image, caption="Uploaded item", use_container_width=True)

            with col_result:
                with st.spinner("Identifying item and retrieving guidance..."):
                    try:
                        from vision_classify import SnapAndSort
                        snap = SnapAndSort(bot=bot)
                        result = snap.analyze(image)

                        st.markdown(f"### {result['item']}")
                        st.caption(f"Category: {result['category']}")
                        st.write(result["guidance"])
                        if result["sources"]:
                            st.caption(f"Retrieved from: {', '.join(result['sources'])}")
                    except Exception as e:
                        st.error(f"Couldn't process that image: {e}")

st.divider()
st.caption(
    "Retrieval: TF-IDF over a curated knowledge base \u00b7 "
    "Generation: grounded LLM answer (or extractive fallback) \u00b7 "
    "Vision: Gemini Vision feeds into the same grounded pipeline \u00b7 "
    "The model never answers outside the retrieved context."
)
