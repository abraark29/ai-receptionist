from flask import Flask, request, jsonify
import openai
import os
import json

app = Flask(__name__)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Debug: confirm key loaded
print("🔐 OpenAI Key Status:", "✔ Loaded" if openai.api_key else "❌ NOT FOUND")

# Debug: list files in working directory
print("📂 Project Files:", os.listdir("."))

# Load knowledge base
try:
    with open("knowledge_base.json", "r") as f:
        kb = json.load(f)
    print("📘 Knowledge base loaded successfully.")
except Exception as e:
    print("❌ Failed to load knowledge_base.json:", e)
    kb = {}

@app.route("/", methods=["GET"])
def home():
    return "AI Receptionist is running."

@app.route("/gpt-response", methods=["POST"])
def gpt_response():
    data = request.get_json()
    user_input = data.get("user_input", "")
    print("📞 User said:", user_input)

    if not user_input:
        print("⚠️ No user_input received.")
        return jsonify({"response": "I'm sorry, I didn’t catch that. Could you repeat that please?"})

    try:
        kb_text = "\n".join([f"{q}: {a}" for q, a in kb.items()])
        system_msg = (
            "You are a helpful receptionist. Use only the knowledge base below. "
            "If the answer is not in the knowledge base, say you will connect the caller to a staff member."
        )

        prompt = f"""Knowledge Base:
{kb_text}

Caller said: "{user_input}"
"""

        print("🧠 GPT Prompt:\n", prompt)

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.5
        )

        reply = response["choices"][0]["message"]["content"].strip()
        print("🤖 GPT reply:", reply)

        return jsonify({"response": reply})

    except Exception as e:
        print("❌ GPT error:", e)
        return jsonify({"response": "Sorry, something went wrong. Let me connect you to a staff member."})

# Render-compatible port binding
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
