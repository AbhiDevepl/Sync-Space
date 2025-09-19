import google.generativeai as genai
from datetime import datetime
import sys
import os

# -----------------------------
# Suppress gRPC/absl warnings
# -----------------------------
class DummyStderr:
    def write(self, _): pass
    def flush(self): pass

# Redirect stderr temporarily
sys.stderr = DummyStderr()

# -----------------------------
# Hardcode your API key
# -----------------------------
API_KEY = "AIzaSyDRI4uwN_lk5c9xW28Tn8B9Rliy14gMrbY"
genai.configure(api_key=API_KEY)

# Restore stderr so errors in code still appear
sys.stderr = sys.__stderr__

# -----------------------------
# Initialize the Gemini model
# -----------------------------
model = genai.GenerativeModel("gemini-2.0-flash")

# -----------------------------
# Prepare log file
# -----------------------------
log_file = "gemini_responses.txt"
print("Enter prompts continuously. Press Ctrl+C to stop.")
print(f"Responses will be saved in {log_file}\n")

# -----------------------------
# Continuous input loop
# -----------------------------
while True:
    try:
        prompt = input(">> ")

        response = model.generate_content(prompt)

        output = f"Response: {response.text}\n{'-'*50}\n"

        print(output)

        with open(log_file, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}]\n{output}")

    except KeyboardInterrupt:
        print("\nProgram stopped by user. Goodbye!")
        break
    except Exception as e:
        print("Error:", e)