from flask import Flask, request
import time
import json
import requests

app = Flask(__name__)

# Instagram credentials (Replace with your actual credentials)
INSTAGRAM_USERNAME = "your_username"
INSTAGRAM_PASSWORD = "your_password"

# Instagram API URLs
LOGIN_URL = "https://www.instagram.com/api/v1/web/accounts/login/"
MESSAGE_URL = "https://www.instagram.com/api/v1/direct_v2/threads/broadcast/text/"

# Create a session for handling requests
session = requests.Session()

def login():
    """Logs into Instagram and maintains the session."""
    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-CSRFToken": session.cookies.get_dict().get("csrftoken", ""),
    }
    payload = {"username": INSTAGRAM_USERNAME, "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:&:{INSTAGRAM_PASSWORD}"}
    
    response = session.post(LOGIN_URL, data=payload, headers=headers)
    
    if response.status_code == 200 and "authenticated" in response.text:
        print("Login successful!")
        return True
    else:
        print("Login failed:", response.text)
        return False

def send_message(thread_id, message):
    """Sends a message to the given Instagram thread ID."""
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": session.cookies.get_dict().get("csrftoken", ""),
    }
    payload = {"thread_id": thread_id, "text": message}
    
    response = session.post(MESSAGE_URL, data=payload, headers=headers)
    
    if response.status_code == 200:
        return "Message sent!"
    return f"Failed to send message: {response.text}"

@app.route("/", methods=["GET", "POST"])
def index():
    """Handles the form submission and message sending process."""
    if request.method == "POST":
        thread_id = request.form.get("thread_id")
        delay = int(request.form.get("delay", 2))
        file = request.files.get("file")

        if file and thread_id:
            messages = file.read().decode().splitlines()
            login_success = login()

            if login_success:
                for message in messages:
                    print(f"Sending message: {message}")
                    result = send_message(thread_id, message)
                    print(result)
                    time.sleep(delay)  # Delay to prevent spam detection
                return "Messages sent successfully!"
            else:
                return "Instagram login failed!"

    # Serve the form directly from Flask
    return """
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Instagram Message Sender</title>
    </head>
    <body>
        <h2>Send Messages to Instagram Thread</h2>
        <form method="POST" enctype="multipart/form-data">
            <label>Thread ID:</label>
            <input type="text" name="thread_id" required><br><br>
            
            <label>Select TXT File:</label>
            <input type="file" name="file" accept=".txt" required><br><br>
            
            <label>Delay (seconds):</label>
            <input type="number" name="delay" min="1" value="2"><br><br>
            
            <button type="submit">Send Messages</button>
        </form>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
