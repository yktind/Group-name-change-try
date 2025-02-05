from flask import Flask, request, redirect, url_for, flash, render_template_string
from instagrapi import Client
import time
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Instagram credentials
USERNAME = "your_username"
PASSWORD = "your_password"

# Initialize Instagram client
cl = Client()

# Login to Instagram
def instagram_login():
    try:
        cl.login(USERNAME, PASSWORD)
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False

# Function to send messages
def send_message(group_chat_id, message, delay):
    try:
        cl.direct_send(message, [group_chat_id])
        time.sleep(delay)  # Delay before next message
        return True
    except Exception as e:
        print(f"Message sending failed: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        group_chat_id = request.form.get('group_chat_id')
        delay = int(request.form.get('delay', 1))  # Default delay 1 second
        
        file = request.files.get('file')
        if not file:
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Read messages from the file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                messages = f.readlines()
        except Exception as e:
            flash(f'Error reading file: {e}', 'error')
            return redirect(url_for('index'))

        # Login to Instagram
        if not instagram_login():
            flash('Instagram login failed!', 'error')
            return redirect(url_for('index'))

        # Send messages
        for message in messages:
            message = message.strip()
            if message:
                send_message(group_chat_id, message, delay)

        flash('Messages sent successfully!', 'success')
        return redirect(url_for('index'))

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Instagram Group Chat Messenger</title>
    </head>
    <body>
        <h2>Instagram Group Chat Messenger</h2>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <p class="{{ category }}">{{ message }}</p>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <form method="POST" enctype="multipart/form-data">
            <label>Group Chat ID:</label>
            <input type="text" name="group_chat_id" required><br><br>

            <label>Select TXT File:</label>
            <input type="file" name="file" accept=".txt" required><br><br>

            <label>Delay (seconds):</label>
            <input type="number" name="delay" min="1" value="1"><br><br>

            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
            
