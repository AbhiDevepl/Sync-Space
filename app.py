from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from datetime import datetime
import sys

# -----------------------------
# Suppress gRPC/absl warnings
# -----------------------------
class DummyStderr:
    def write(self, _): pass
    def flush(self): pass

sys.stderr = DummyStderr()

# -----------------------------
# Configure Gemini AI
# -----------------------------
API_KEY = "AIzaSyDRI4uwN_lk5c9xW28Tn8B9Rliy14gMrbY"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

sys.stderr = sys.__stderr__

# -----------------------------
# Flask app
# -----------------------------
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data.get("prompt", "")
    
    try:
        response = model.generate_content(prompt)
        answer = response.text

        # Save log
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("gemini_responses.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}]\nPrompt: {prompt}\nResponse: {answer}\n{'-'*50}\n")

        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)