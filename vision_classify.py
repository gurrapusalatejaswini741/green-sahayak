"""
vision_classify.py
-------------------
"Snap & Sort" - the multimodal differentiator for GreenSahayak.
 
Takes a photo of an item (waste, packaging, an old device, etc.) and:
  1. Asks Gemini Vision to identify what it is and which disposal
     category it likely belongs to (wet/dry/recyclable/hazardous/e-waste)
  2. Feeds that identification into the SAME RAG pipeline used for text
     questions (retrieval.py + rag_chat.py), so the disposal guidance
     the user gets is grounded in the same curated knowledge base -
     not a separate, unverified vision-model guess.
 
This requires a Gemini API key (see README) since real image
understanding has no honest offline fallback. If no key is set, the
UI should disable this feature and point the user to text chat instead
rather than pretending to classify the image.
"""
 
import os
import io
import base64
from PIL import Image
 
from rag_chat import GreenSahayak
 
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
 
VISION_SYSTEM_PROMPT = """You are an item identifier for a household waste-sorting assistant in
India. You will be shown a photo of a single item. Respond in this exact format, nothing else:
 
ITEM: <short name of the item, e.g. "plastic water bottle", "used AA battery", "banana peel">
CATEGORY: <one of: wet/biodegradable, dry/recyclable, hazardous, e-waste, unclear>
QUERY: <a short natural-language question a person would ask about disposing of this item,
        e.g. "how do I dispose of a plastic water bottle">
 
If you cannot clearly identify the item, set CATEGORY to unclear and write a QUERY asking
generally about safe disposal of unidentified household waste."""
 
 
def classify_image(image: Image.Image) -> dict:
    """
    Returns {"item": str, "category": str, "query": str} or raises if the
    API call fails (caller should handle this and show a clear error,
    not a silent guess).
    """
    if not GEMINI_API_KEY:
        raise RuntimeError("No GEMINI_API_KEY configured - image classification needs it.")
 
    from google import genai
 
    # Encode the PIL image as base64 JPEG for the Interactions API's inline
    # image input format.
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="JPEG")
    image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
 
    client = genai.Client(api_key=GEMINI_API_KEY)
    interaction = client.interactions.create(
        model="gemini-3-flash-preview",
        system_instruction=VISION_SYSTEM_PROMPT,
        input=[
            {"type": "text", "text": "Identify this item."},
            {"type": "image", "data": image_b64, "mime_type": "image/jpeg"},
        ],
    )
    text = interaction.output_text.strip()
 
    result = {"item": "unknown item", "category": "unclear", "query": "how do I safely dispose of household waste"}
    for line in text.splitlines():
        if line.upper().startswith("ITEM:"):
            result["item"] = line.split(":", 1)[1].strip()
        elif line.upper().startswith("CATEGORY:"):
            result["category"] = line.split(":", 1)[1].strip()
        elif line.upper().startswith("QUERY:"):
            result["query"] = line.split(":", 1)[1].strip()
    return result
 
 
class SnapAndSort:
    """Combines vision classification with the existing RAG pipeline."""
 
    def __init__(self, bot: GreenSahayak = None):
        self.bot = bot or GreenSahayak()
 
    def analyze(self, image: Image.Image) -> dict:
        classification = classify_image(image)
        rag_result = self.bot.ask(classification["query"])
        return {
            "item": classification["item"],
            "category": classification["category"],
            "guidance": rag_result["answer"],
            "sources": rag_result["sources"],
            "mode": rag_result["mode"],
        }
 
 
if __name__ == "__main__":
    print("This module requires an image input and a GEMINI_API_KEY to test live.")
    print(f"API key configured: {bool(GEMINI_API_KEY)}")
 
