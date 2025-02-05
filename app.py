from flask import Flask, request, flash, redirect, url_for
from instagrapi import Client
import time
import threading
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Instagram login function
def login_instagram(username, password):
    cl = Client()
    try:
        cl.login(username, password)
        return cl
    except Exception as e:
        return str(e)

# Function to send messages from a .txt file
def send_messages(cl, group_chat_id, file_path, delay):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            messages = file.readlines()

        for msg in messages:
            cl.direct_send(msg.strip(), [], thread_id=group_chat_id)
            time.sleep(delay)

        flash("Messages sent successfully!", "success")
    except Exception as e:
        flash(str(e), "danger")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        group_chat_id = request.form["group_chat_id"]
        delay = int(request.form["delay"])
        file = request.files["txt_file"]

        if file:
            file_path = "messages.txt"
            file.save(file_path)

            cl = login_instagram(username, password)
            if isinstance(cl, Client):
                threading.Thread(target=send_messages, args=(cl, group_chat_id, file_path, delay)).start()
                flash("Sending messages in the background!", "info")
            else:
                flash("Login failed: " + cl, "danger")
            
            # Clean up by removing the uploaded file after processing
            os.remove(file_path)

    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Instagram Group Message Sender</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css">
        <style>
            body {
                background: url('https://source.unsplash.com/random/1600x900') no-repeat center center fixed;
                background-size: cover;
            }
            .container {
                margin-top: 100px;
                background: rgba(0, 0, 0, 0.7);
                padding: 30px;
                border-radius: 10px;
                color: white;
                box-shadow: 0px 0px 10px rgba(255, 255, 255, 0.5);
            }
            h2 {
                animation: fadeIn 2s ease-in-out;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2 class="text-center">Instagram Group Message Sender</h2>
            <form action="/" method="POST" enctype="multipart/form-data">
                <div class="mb-3">
                    <label for="username" class="form-label">Instagram Username</label>
                    <input type="text" class="form-control" id="username" name="username" required>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Instagram Password</label>
                    <input type="password" class="form-control" id="password" name="password" required>
                </div>
                <div class="mb-3">
                    <label for="group_chat_id" class="form-label">Group Chat ID</label>
                    <input type="text" class="form-control" id="group_chat_id" name="group_chat_id" required>
                </div>
                <div class="mb-3">
                    <label for="txt_file" class="form-label">Select Text File</label>
                    <input type="file" class="form-control" id="txt_file" name="txt_file" accept=".txt" required>
                </div>
                <div class="mb-3">
                    <label for="delay" class="form-label">Message Delay (Seconds)</label>
                    <input type="number" class="form-control" id="delay" name="delay" min="1" required>
                </div>
                <button type="submit" class="btn btn-primary w-100">Submit</button>
            </form>
        </div>
    </body>
    </html>
    '''
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
