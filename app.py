from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# Simple rule-based demo classifier.
# For a college project, this can later be replaced with a trained ML model.
CYBERBULLYING_WORDS = {
    "idiot", "stupid", "loser", "ugly", "hate you", "shut up",
    "worthless", "dumb", "fool", "moron", "trash"
}

SPAM_WORDS = {
    "free", "win", "winner", "prize", "offer", "click here",
    "urgent", "claim now", "limited time", "congratulations",
    "lottery", "cash", "discount", "subscribe", "bonus"
}

def normalize(text):
    return re.sub(r"\s+", " ", text.lower().strip())

def detect_text(text):
    text = normalize(text)

    if not text:
        return {"label": "Normal", "confidence": 0, "reason": "Please enter some text."}

    cyber_hits = [w for w in CYBERBULLYING_WORDS if w in text]
    spam_hits = [w for w in SPAM_WORDS if w in text]

    # Extra spam signals
    url_count = len(re.findall(r"https?://|www\.", text))
    exclamations = text.count("!")
    caps_words = len(re.findall(r"\b[A-Z]{4,}\b", text))

    cyber_score = min(0.95, 0.55 + 0.12 * len(cyber_hits)) if cyber_hits else 0
    spam_score = min(0.97, 0.50 + 0.10 * len(spam_hits) + 0.08 * url_count +
                     0.04 * min(exclamations, 4) + 0.04 * min(caps_words, 3))

    if cyber_score > spam_score and cyber_score >= 0.55:
        return {
            "label": "Cyberbullying",
            "confidence": round(cyber_score * 100),
            "reason": "Potentially abusive or insulting language detected."
        }
    elif spam_score >= 0.55:
        return {
            "label": "Spam",
            "confidence": round(spam_score * 100),
            "reason": "Promotional, urgent, suspicious, or repetitive spam-like signals detected."
        }
    else:
        return {
            "label": "Normal",
            "confidence": 90,
            "reason": "No strong spam or cyberbullying signals detected."
        }

@app.route("/")
def home():
    return render_template("index.html")

@app.post("/predict")
def predict():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    return jsonify(detect_text(text))

if __name__ == "__main__":
    app.run(debug=True)
