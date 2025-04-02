from flask import Flask, request, render_template_string
import time
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>SayHi Bot</title>
</head>
<body>
    <h2>Send Message</h2>
    <form action="/" method="post" enctype="multipart/form-data">
        <label>Email:</label>
        <input type="email" name="email" required><br>
        
        <label>Chat ID:</label>
        <input type="text" name="chat_id" required><br>
        
        <label>Message:</label>
        <textarea name="message" required></textarea><br>
        
        <label>Select File:</label>
        <input type="file" name="file"><br>
        
        <label>Delay (seconds):</label>
        <input type="number" name="delay" min="0" required><br>
        
        <button type="submit">Send</button>
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        chat_id = request.form['chat_id']
        message = request.form['message']
        delay = int(request.form['delay'])
        
        file = request.files['file']
        if file and file.filename:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            with open(file_path, 'r') as f:
                file_contents = f.read()
            message += f"\n\n{file_contents}"
        
        send_message(email, chat_id, message, delay)
        return 'Message sent successfully!'
    
    return render_template_string(HTML_FORM)

def send_message(email, chat_id, message, delay):
    print(f"Logging in with {email}...")
    time.sleep(2)  # Simulate login delay
    print(f"Sending message to chat ID {chat_id}...")
    time.sleep(delay)
    print(f"Message sent: {message}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
