from flask import Flask, request, redirect, url_for, session
from instagrapi import Client
import time
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Ensure the uploads directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Instagram login function
def login_instagram(username, password):
    cl = Client()
    try:
        cl.login(username, password)
        return cl
    except Exception as e:
        return str(e)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        thread_id = request.form["thread_id"]
        delay = int(request.form["delay"])
        mention_name = request.form["mention_name"]

        file = request.files["message_file"]
        if file:
            filepath = os.path.join("uploads", file.filename)
            file.save(filepath)

        session["username"] = username
        session["password"] = password
        session["thread_id"] = thread_id
        session["delay"] = delay
        session["mention_name"] = mention_name
        session["filepath"] = filepath

        return redirect(url_for("send_message"))

    return '''
        <html>
        <head><title>Instagram Auto Messaging</title></head>
        <body>
            <h2>Instagram Auto Messaging</h2>
            <form method="POST" enctype="multipart/form-data">
                <label>Username:</label>
                <input type="text" name="username" required><br><br>
                
                <label>Password:</label>
                <input type="password" name="password" required><br><br>
                
                <label>Thread ID:</label>
                <input type="text" name="thread_id" required><br><br>
                
                <label>Mention Name:</label>
                <input type="text" name="mention_name" required><br><br>
                
                <label>Message File (TXT):</label>
                <input type="file" name="message_file" accept=".txt" required><br><br>
                
                <label>Delay (seconds):</label>
                <input type="number" name="delay" required><br><br>
                
                <button type="submit">Start Messaging</button>
            </form>
        </body>
        </html>
    '''

@app.route("/send_message")
def send_message():
    username = session.get("username")
    password = session.get("password")
    thread_id = session.get("thread_id")
    delay = session.get("delay")
    mention_name = session.get("mention_name")
    filepath = session.get("filepath")

    cl = login_instagram(username, password)
    if not isinstance(cl, Client):
        return f"Login failed: {cl}"

    # Read messages from TXT file
    with open(filepath, "r") as f:
        messages = f.readlines()

    for message in messages:
        formatted_message = f"@{mention_name} {message.strip()}"
        try:
            cl.direct_send(formatted_message, [thread_id])
            time.sleep(delay)
        except Exception as e:
            return f"Error sending message: {e}"

    return "Messages sent successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
