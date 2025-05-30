from flask import Flask, request, jsonify
import openai
import os
import json

app = Flask(__name__)

# Load your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the knowledge base once on startup
with open("knowledge_base.json", "r") as f:
    kb = json.load(f)

@app.route("/", methods=["GET"])
def home():
    return "AI Receptionist is running."

@app.route("/gpt-response", methods=["POST"])
def gpt_response():
    data = request.get_json()
    user_input = data.get("user_input", "")

    try:
        # Convert KB into plain-text format
        kb_text = "\n".join([f"{q}: {a}" for q, a in kb.items()])

        # GPT role prompt
        system_msg = (
            "You are a helpful and polite receptionist for a medical or dental office. "
            "Use the following knowledge base to answer the caller’s question. "
            "If you're unsure, say you'll connect them to a staff member."
        )

        # Build the GPT prompt with KB and caller message
        prompt = f"""Knowledge Base:
{kb_text}

Caller said: "{user_input}"
Please respond using the knowledge base above.
"""

        # Send to GPT
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user"
