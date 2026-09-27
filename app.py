from flask import Flask, request, render_template_string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

# ---------------------------------------------------
# TRAINING DATA
# ---------------------------------------------------

messages = [
    # NORMAL
    "Hello how are you",
    "I am fine",
    "I am good",
    "How are you",
    "Good morning",
    "Good afternoon",
    "Good evening",
    "Have a nice day",
    "Nice to meet you",
    "Thank you",
    "You are my friend",
    "You are a good friend",
    "Let's study together",
    "Can you help me with my homework",
    "I am going to college",
    "See you tomorrow",
    "What are you doing",
    "Are you coming to college",
    "I will call you later",
    "Have a good day",
    "I am studying",
    "Let's meet tomorrow",
    "Can you send me the notes",
    "Please help me",
    "I completed my assignment",
    "The class was good",
    "Today is a beautiful day",
    "I am happy today",
    "Nice work",
    "Well done",

    # SPAM
    "Congratulations you won a lottery",
    "You have won a prize",
    "Click this link to win money",
    "You are selected for a free gift",
    "Claim your free prize now",
    "Win a free iPhone",
    "You have won 10000 dollars",
    "Click now to get your reward",
    "Limited time offer click here",
    "Get free cash now",
    "Congratulations claim your reward",
    "You are a lucky winner",
    "Free gift waiting for you",
    "Click the link and win",
    "Exclusive discount offer",
    "Buy now and get free gifts",
    "You have been selected for a special offer",
    "Earn money quickly",
    "Get rich quickly",
    "Free recharge available click now",

    # CYBERBULLYING
    "You are stupid",
    "You are an idiot",
    "Nobody likes you",
    "You are useless",
    "You are so dumb",
    "I hate you",
    "You are a loser",
    "Shut up idiot",
    "You are worthless",
    "Everyone hates you",
    "You are annoying",
    "You cannot do anything",
    "You are dumb",
    "Go away loser",
    "You are pathetic",
    "Nobody wants you here",
    "You are a fool",
    "I don't like you",
    "You are terrible",
    "Stop bothering everyone"
]

labels = (
    ["Normal"] * 30 +
    ["Spam"] * 20 +
    ["Cyberbullying"] * 20
)

# ---------------------------------------------------
# MACHINE LEARNING MODEL
# ---------------------------------------------------

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(messages)

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(X, labels)

# ---------------------------------------------------
# HTML PAGE
# ---------------------------------------------------

HTML = """
<!DOCTYPE html>
<html>
<head>

    <title>AI Cyberbullying & Spam Detection</title>

    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            color: #222;
        }

        .header {
            background: #1f2937;
            color: white;
            text-align: center;
            padding: 25px 15px;
        }

        .header h1 {
            margin: 0;
            font-size: 28px;
        }

        .header p {
            margin-top: 8px;
            font-size: 15px;
            color: #d1d5db;
        }

        .container {
            width: 90%;
            max-width: 900px;
            margin: 35px auto;
        }

        .card {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }

        textarea {
            width: 100%;
            height: 130px;
            padding: 15px;
            border: 1px solid #ccc;
            border-radius: 8px;
            resize: none;
            font-size: 16px;
            outline: none;
        }

        textarea:focus {
            border-color: #374151;
        }

        button {
            width: 100%;
            margin-top: 15px;
            padding: 14px;
            border: none;
            border-radius: 8px;
            background: #1f2937;
            color: white;
            font-size: 17px;
            cursor: pointer;
        }

        button:hover {
            background: #111827;
        }

        .result {
            margin-top: 30px;
            padding: 22px;
            border: 1px solid #ddd;
            border-radius: 10px;
            background: #fafafa;
        }

        .prediction {
            font-size: 25px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }

        .confidence {
            text-align: center;
            font-size: 19px;
            margin-bottom: 25px;
        }

        .chart-title {
            font-size: 19px;
            font-weight: bold;
            margin-bottom: 18px;
        }

        .bar-row {
            margin-bottom: 18px;
        }

        .bar-label {
            display: flex;
            justify-content: space-between;
            margin-bottom: 6px;
            font-size: 15px;
        }

        .bar-background {
            width: 100%;
            height: 25px;
            background: #e5e7eb;
            border-radius: 5px;
            overflow: hidden;
        }

        .bar {
            height: 100%;
            border-radius: 5px;
        }

        .normal {
            background: #4b5563;
        }

        .spam {
            background: #6b7280;
        }

        .cyber {
            background: #374151;
        }

        .info {
            margin-top: 25px;
            padding: 15px;
            background: #f3f4f6;
            border-radius: 8px;
            font-size: 14px;
            line-height: 1.6;
        }

        .footer {
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 13px;
        }

        @media(max-width:600px) {

            .header h1 {
                font-size: 22px;
            }

            .card {
                padding: 20px;
            }

        }

    </style>

</head>

<body>

    <div class="header">

        <h1>AI-Based Cyberbullying & Spam Detection System</h1>

        <p>
            Machine Learning based text classification system
        </p>

    </div>


    <div class="container">

        <div class="card">

            <h2>Enter Your Message</h2>

            <form method="POST">

                <textarea
                    name="message"
                    placeholder="Enter a message to analyze..."
                    required
                >{{ message }}</textarea>

                <button type="submit">
                    Detect Message
                </button>

            </form>


            {% if prediction %}

            <div class="result">

                <div class="prediction">

                    Prediction: {{ prediction }}

                </div>


                <div class="confidence">

                    Confidence Level:
                    <strong>{{ confidence }}%</strong>

                </div>


                <div class="chart-title">

                    Confidence Level Bar Graph

                </div>


                <!-- NORMAL -->

                <div class="bar-row">

                    <div class="bar-label">

                        <span>Normal</span>

                        <span>{{ normal_conf }}%</span>

                    </div>

                    <div class="bar-background">

                        <div
                            class="bar normal"
                            style="width: {{ normal_conf }}%;">
                        </div>

                    </div>

                </div>


                <!-- SPAM -->

                <div class="bar-row">

                    <div class="bar-label">

                        <span>Spam</span>

                        <span>{{ spam_conf }}%</span>

                    </div>

                    <div class="bar-background">

                        <div
                            class="bar spam"
                            style="width: {{ spam_conf }}%;">
                        </div>

                    </div>

                </div>


                <!-- CYBERBULLYING -->

                <div class="bar-row">

                    <div class="bar-label">

                        <span>Cyberbullying</span>

                        <span>{{ cyber_conf }}%</span>

                    </div>

                    <div class="bar-background">

                        <div
                            class="bar cyber"
                            style="width: {{ cyber_conf }}%;">
                        </div>

                    </div>

                </div>


                <div class="info">

                    <strong>How it works:</strong><br>

                    The entered message is converted into numerical
                    features using TF-IDF. The Logistic Regression
                    machine learning model then predicts whether the
                    message is Normal, Spam, or Cyberbullying.

                    The confidence values show the model's estimated
                    probability for each category.

                </div>

            </div>

            {% endif %}

        </div>

    </div>


    <div class="footer">

        AI-Based Cyberbullying & Spam Detection System

    </div>

</body>
</html>
"""


# ---------------------------------------------------
# FLASK ROUTE
# ---------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    confidence = 0

    normal_conf = 0
    spam_conf = 0
    cyber_conf = 0

    message = ""

    if request.method == "POST":

        message = request.form.get("message", "").strip()

        if message:

            # Convert message into TF-IDF
            message_vector = vectorizer.transform([message])

            # Prediction
            prediction = model.predict(message_vector)[0]

            # Probability
            probabilities = model.predict_proba(message_vector)[0]

            classes = model.classes_

            # Create probability dictionary
            probability_dict = dict(
                zip(classes, probabilities)
            )

            # Get confidence values
            normal_conf = round(
                probability_dict.get("Normal", 0) * 100,
                2
            )

            spam_conf = round(
                probability_dict.get("Spam", 0) * 100,
                2
            )

            cyber_conf = round(
                probability_dict.get("Cyberbullying", 0) * 100,
                2
            )

            # Highest probability
            confidence = round(
                max(probabilities) * 100,
                2
            )

    return render_template_string(
        HTML,
        prediction=prediction,
        confidence=confidence,
        normal_conf=normal_conf,
        spam_conf=spam_conf,
        cyber_conf=cyber_conf,
        message=message
    )


# ---------------------------------------------------
# RUN APPLICATION
# ---------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )