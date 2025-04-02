from flask import Flask, request, redirect, url_for, session, render_template_string
from instagrapi import Client
import time
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a strong secret key

# Instagram Client
cl = Client()

def send_messages(username, password, thread_id, message_file, delay, image_path):
    try:
        cl.login(username, password)
        
        with open(message_file, 'r', encoding='utf-8') as file:
            messages = file.readlines()
            
        for msg in messages:
            msg = msg.strip()
            if msg:
                cl.direct_send(msg, thread_ids=[thread_id])
                time.sleep(delay)
                
        if image_path and os.path.exists(image_path):
            cl.direct_send_photo(image_path, thread_ids=[thread_id])
        
        return "Messages Sent Successfully"
    except Exception as e:
        return str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        thread_id = request.form['thread_id']
        delay = int(request.form['delay'])
        
        if 'message_file' not in request.files:
            return "No file selected"
        
        file = request.files['message_file']
        file_path = f"uploads/{file.filename}"
        file.save(file_path)
        
        image_path = None
        if 'image' in request.files:
            image = request.files['image']
            if image.filename:
                image_path = f"uploads/{image.filename}"
                image.save(image_path)
        
        session['status'] = send_messages(username, password, thread_id, file_path, delay, image_path)
        return redirect(url_for('index'))
    
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Instagram Messenger</title>
    </head>
    <body>
        <h2>Instagram Auto Messenger</h2>
        {% if status %}
            <p>{{ status }}</p>
        {% endif %}
        <form method="post" enctype="multipart/form-data">
            <label>Instagram Username:</label>
            <input type="text" name="username" required><br>
            <label>Password:</label>
            <input type="password" name="password" required><br>
            <label>Target Thread ID:</label>
            <input type="text" name="thread_id" required><br>
            <label>Delay (seconds):</label>
            <input type="number" name="delay" required><br>
            <label>Select TXT File:</label>
            <input type="file" name="message_file" accept=".txt" required><br>
            <label>Background Image (optional):</label>
            <input type="file" name="image" accept="image/*"><br>
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    ''', status=session.pop('status', None))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
