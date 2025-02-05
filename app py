import os
import time
import threading
from flask import Flask, request, render_template_string, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this for security

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dummy credentials (Replace with a secure method in production)
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

# Store thread info
worker_thread = None

# HTML template (since you don’t want index.html)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Message Sender</title>
</head>
<body>
    {% if not session.get('logged_in') %}
        <h2>Login</h2>
        <form method="POST" action="/login">
            <label>Username:</label>
            <input type="text" name="username" required>
            <br><br>
            <label>Password:</label>
            <input type="password" name="password" required>
            <br><br>
            <input type="submit" value="Login">
        </form>
    {% else %}
        <h2>Upload a TXT file</h2>
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" accept=".txt" required>
            <br><br>
            <label>Delay (seconds):</label>
            <input type="number" name="delay" min="1" required>
            <br><br>
            <input type="submit" value="Submit">
        </form>
        <br>
        <form action="/logout" method="POST">
            <input type="submit" value="Logout">
        </form>
    {% endif %}
</body>
</html>
"""

def send_messages(file_path, delay):
    """Worker thread function to send messages with a delay."""
    with open(file_path, "r") as file:
        for line in file:
            print(f"Sending message: {line.strip()}")
            time.sleep(delay)

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        session["logged_in"] = True
        return redirect(url_for("home"))
    return "Invalid credentials. <a href='/'>Try again</a>"

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("home"))

@app.route("/upload", methods=["POST"])
def upload():
    if not session.get("logged_in"):
        return redirect(url_for("home"))
    
    file = request.files.get("file")
    delay = request.form.get("delay")

    if not file or not delay:
        return "Missing file or delay value. <a href='/'>Go back</a>"

    delay = int(delay)

    if file.filename.endswith(".txt"):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        global worker_thread
        worker_thread = threading.Thread(target=send_messages, args=(file_path, delay))
        worker_thread.start()

        return "File uploaded and messages are being sent. <a href='/'>Go back</a>"
    return "Only .txt files are allowed. <a href='/'>Try again</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
