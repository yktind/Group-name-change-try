from flask import Flask, request, render_template_string
from instagrapi import Client
import time
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Instagram Login Credentials
INSTAGRAM_USERNAME = "monksalutoi"
INSTAGRAM_PASSWORD = "g-223344"

# Target Group Chat (Thread ID)
TARGET_THREAD_ID = "9430891733632883"

# Initialize Instagram Client
cl = Client()

def login():
    try:
        cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        return True
    except Exception as e:
        print("Login failed:", e)
        return False

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        
        file = request.files["file"]
        
        if file.filename == "":
            return "No selected file"
        
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    message = f.read()
            except Exception as e:
                return f"Error reading file: {e}"

            # Delay in seconds (modify as needed)
            delay = int(request.form.get("delay", 5))

            if login():
                try:
                    time.sleep(delay)
                    cl.direct_send(message, [], thread_ids=[TARGET_THREAD_ID])
                    return "Message sent successfully!"
                except Exception as e:
                    return f"Error sending message: {e}"
            else:
                return "Instagram login failed."

    return '''
    <!doctype html>
    <title>Upload a Text File</title>
    <h1>Upload a Text File to Send as an Instagram Message</h1>
    <form action="/" method="post" enctype="multipart/form-data">
        <input type="file" name="file"><br><br>
        <label for="delay">Delay (seconds):</label>
        <input type="number" name="delay" value="5" min="0"><br><br>
        <input type="submit" value="Upload and Send">
    </form>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
            
