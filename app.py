from flask import Flask, request, render_template_string
import time
import requests

app = Flask(__name__)

# Instagram login credentials (set manually or via a config file)
INSTAGRAM_USERNAME = "your_username"
INSTAGRAM_PASSWORD = "your_password"
TARGET_THREAD_ID = "your_target_thread_id"

# Instagram API Endpoints
LOGIN_URL = "https://www.instagram.com/api/v1/accounts/login/"
SEND_MESSAGE_URL = f"https://www.instagram.com/api/v1/direct_v2/threads/{TARGET_THREAD_ID}/items/"

# Session Storage
session = requests.Session()

def login_instagram():
    """Log in to Instagram and store the session cookies."""
    payload = {
        "username": INSTAGRAM_USERNAME,
        "password": INSTAGRAM_PASSWORD
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = session.post(LOGIN_URL, data=payload, headers=headers)
    
    if response.status_code == 200:
        print("[+] Login Successful!")
        return True
    else:
        print("[-] Login Failed:", response.json())
        return False

def send_message(text):
    """Send a message to the target thread."""
    payload = {
        "text": text
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = session.post(SEND_MESSAGE_URL, data=payload, headers=headers)
    
    if response.status_code == 200:
        return "[+] Message Sent!"
    else:
        return "[-] Message Failed:", response.json()

HTML_FORM = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Message Sender</title>
</head>
<body>
    <h2>Send Instagram Message</h2>
    <form action="/" method="POST" enctype="multipart/form-data">
        <label>Select Text File:</label>
        <input type="file" name="file" accept=".txt" required><br><br>
        
        <label>Delay (seconds):</label>
        <input type="number" name="delay" min="1" required><br><br>

        <button type="submit">Send Message</button>
    </form>
    <p>{{ message_status }}</p>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    message_status = ""
    
    if request.method == "POST":
        file = request.files["file"]
        delay = int(request.form["delay"])
        
        if file:
            text = file.read().decode("utf-8")
            time.sleep(delay)  # Delay before sending
            message_status = send_message(text)
    
    return render_template_string(HTML_FORM, message_status=message_status)

if __name__ == "__main__":
    if login_instagram():
        app.run(host="0.0.0.0", port=5000, debug=True)
        
