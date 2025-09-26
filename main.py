from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "secret123"  # Needed for sessions

# Difficulty levels
LEVELS = {
    1: 3,   # 3 digits
    2: 5,   # 5 digits
    3: 7,   # 7 digits
    4: 9,   # 9 digits
    5: 12   # 12 digits
}

@app.route("/", methods=["GET", "POST"])
def index():
    if "level" not in session:
        session["level"] = 1
    if "score" not in session:
        session["score"] = 0

    sequence = None
    result = None

    if request.method == "POST":
        user_answer = request.form["answer"]
        correct_sequence = session["sequence"]

        if user_answer == correct_sequence:
            session["score"] += 1
            session["level"] = min(session["level"] + 1, 5)
            result = "✅ Correct! Difficulty increased!"
        else:
            session["score"] = max(session["score"] - 1, 0)
            session["level"] = max(session["level"] - 1, 1)
            result = f"❌ Wrong! The correct sequence was {correct_sequence}"

    # Generate a new sequence based on level
    length = LEVELS[session["level"]]
    sequence = "".join(str(random.randint(0, 9)) for _ in range(length))
    session["sequence"] = sequence

    return render_template("index.html", sequence=sequence, level=session["level"], score=session["score"], result=result)

if __name__ == "__main__":
    app.run(debug=True)
