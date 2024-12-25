from flask import Flask, request, render_template, redirect, url_for
from instagrapi import Client
import time
import threading

# Flask app initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Global variables
client = None
is_running = False
stop_flag = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    global client
    username = request.form['username']
    password = request.form['password']
    client = Client()

    try:
        client.login(username, password)
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Login failed: {str(e)}"

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/send_messages', methods=['POST'])
def send_messages():
    global is_running, stop_flag

    if is_running:
        return "A process is already running!"

    file = request.files['txt_file']
    delay = int(request.form['delay'])
    hater_username = request.form['hater_username']

    if file:
        usernames = file.read().decode('utf-8').splitlines()
        stop_flag = False

        def message_sender():
            global is_running, stop_flag
            is_running = True

            for username in usernames:
                if stop_flag:
                    break
                try:
                    client.direct_send(f"Hi {username}, this is a message from the script!", username)
                    print(f"Message sent to {username}")
                except Exception as e:
                    print(f"Failed to send message to {username}: {str(e)}")
                time.sleep(delay)

            is_running = False

        threading.Thread(target=message_sender).start()
        return "Messages are being sent in the background!"
    else:
        return "No file uploaded!"

@app.route('/stop', methods=['POST'])
def stop():
    global stop_flag
    stop_flag = True
    return "Stopping the current process."

# HTML Templates
index_html = """
<!doctype html>
<html>
    <head>
        <title>Instagram Login</title>
    </head>
    <body>
        <h1>Login to Instagram</h1>
        <form action="/login" method="POST">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Login</button>
        </form>
    </body>
</html>
"""

dashboard_html = """
<!doctype html>
<html>
    <head>
        <title>Dashboard</title>
    </head>
    <body>
        <h1>Send Messages</h1>
        <form action="/send_messages" method="POST" enctype="multipart/form-data">
            <label for="txt_file">Upload Text File (Usernames):</label>
            <input type="file" name="txt_file" required><br>
            <label for="hater_username">Hater's Username:</label>
            <input type="text" name="hater_username" required><br>
            <label for="delay">Delay (seconds):</label>
            <input type="number" name="delay" min="1" required><br>
            <button type="submit">Send Messages</button>
        </form>
        <form action="/stop" method="POST">
            <button type="submit">Stop</button>
        </form>
    </body>
</html>
"""

@app.route('/styles.css')
def styles():
    return """
        body {
            background: rgb(220, 240, 255);
            font-family: Arial, sans-serif;
        }
        form {
            margin: 20px;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 10px;
            background: #fff;
        }
        button {
            background: lightblue;
            border: none;
            padding: 10px 15px;
            cursor: pointer;
            border-radius: 5px;
        }
        button:hover {
            background: deepskyblue;
        }
    """

@app.before_first_request
def setup_templates():
    # Create templates dynamically
    with open('templates/index.html', 'w') as f:
        f.write(index_html)
    with open('templates/dashboard.html', 'w') as f:
        f.write(dashboard_html)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
        
