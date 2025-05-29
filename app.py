from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/gpt-response", methods=["POST"])
def gpt_response():
    data = request.get_json()
    user_input = data.get("user_input", "")
    caller = data.get("caller", "Unknown caller")

    # Construct the prompt for GPT-4o
    prompt = f"""
You are a virtual receptionist for a doctor's office. Based on the patient's statement below, respond helpfully and professionally.
If they mention pain, bleeding, fever, or other medical concerns, advise them you will transfer to a staff member.
Patient: "{user_input}"
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful medical office assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.5
        )
        reply = response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("GPT error:", e)
        reply = "Sorry, something went wrong. Let me connect you to a staff member."

    return jsonify({"response": reply})

@app.route("/", methods=["GET"])
def home():
    return "AI Receptionist Webhook is Live"

# 🔧 This line ensures Flask works on Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
