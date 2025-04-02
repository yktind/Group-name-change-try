from flask import Flask, request, send_from_directory
from instagrapi import Client
import threading
import time
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Global variables for Instagram client
cl = Client()

# Login function
def login_instagram(username, password):
    try:
        cl.login(username, password)
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False

# Function to send messages with delay
def send_messages(target_file, message, delay, mention_name):
    try:
        with open(target_file, "r") as f:
            thread_ids = [line.strip() for line in f if line.strip()]

        for thread_id in thread_ids:
            try:
                mention_text = f"@{mention_name} {message}" if mention_name else message
                cl.direct_send(mention_text, thread_ids=[thread_id])
                print(f"Message sent to {thread_id}")
                time.sleep(delay)  # Delay between messages
            except Exception as e:
                print(f"Failed to send message to {thread_id}: {e}")
    except Exception as e:
        print(f"Error reading file: {e}")

# Route for home page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        message = request.form["message"]
        mention_name = request.form.get("mention_name", "")
        delay = int(request.form["delay"])

        # File upload handling
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        # Login
        if not login_instagram(username, password):
            return "Login failed. Check credentials."

        # Start message sending in a separate thread
        thread = threading.Thread(target=send_messages, args=(filepath, message, delay, mention_name))
        thread.start()

        return "Message sending started!"

    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Instagram Automation</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            form { background: rgba(255, 255, 255, 0.8); padding: 20px; border-radius: 10px; display: inline-block; }
            input, button { margin: 10px; padding: 10px; }
        </style>
    </head>
    <body>
        <h2>Instagram Message Sender</h2>
        <form action="/" method="post" enctype="multipart/form-data">
            <input type="text" name="username" placeholder="Instagram Username" required><br>
            <input type="password" name="password" placeholder="Instagram Password" required><br>
            <input type="file" name="file" accept=".txt" required><br>
            <input type="text" name="message" placeholder="Enter Message" required><br>
            <input type="text" name="mention_name" placeholder="Mention Username (Optional)"><br>
            <input type="number" name="delay" placeholder="Delay (seconds)" required><br>
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    '''

# Serving uploaded files
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
