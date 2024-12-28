from flask import Flask, request, render_template_string, flash, redirect, url_for
from instagrapi import Client
import time
import threading

app = Flask(__name__)
app.secret_key = "your_secret_key"

# To control the message-sending loop
stop_flag = False

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Group Message Sender</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #ff7e5f, #feb47b);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            max-width: 400px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-weight: bold;
            margin: 10px 0 5px;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background: linear-gradient(45deg, #ff416c, #ff4b2b);
            color: #fff;
            border: none;
            cursor: pointer;
            transition: 0.3s ease;
        }
        button:hover {
            background: linear-gradient(45deg, #ff4b2b, #ff416c);
            transform: scale(1.05);
        }
        .stop-button {
            background: linear-gradient(45deg, #00c6ff, #0072ff);
        }
        .stop-button:hover {
            background: linear-gradient(45deg, #0072ff, #00c6ff);
            transform: scale(1.05);
        }
        .info {
            font-size: 12px;
            color: #777;
            margin-bottom: -10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Group Messenger</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="group_id">Group Thread ID:</label>
            <input type="text" id="group_id" name="group_id" placeholder="Enter group thread ID" required>

            <label for="message_file">Message File:</label>
            <input type="file" id="message_file" name="message_file" required>
            <p class="info">Upload a file containing messages, one per line.</p>

            <label for="delay">Delay (seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay in seconds" required>

            <button type="submit">Send Messages</button>
        </form>
        <form action="/stop" method="POST">
            <button type="submit" class="stop-button">Stop Sending</button>
        </form>
    </div>
</body>
</html>
'''

# Flask Route
@app.route("/", methods=["GET", "POST"])
def send_messages():
    global stop_flag
    stop_flag = False

    if request.method == "POST":
        try:
            # Get form data
            username = request.form["username"]
            password = request.form["password"]
            group_id = request.form["group_id"]
            delay = int(request.form["delay"])
            message_file = request.files["message_file"]

            # Validate message file
            messages = message_file.read().decode("utf-8").splitlines()
            if not messages:
                flash("Message file is empty!", "error")
                return redirect(url_for("send_messages"))

            # Login to Instagram
            cl = Client()
            try:
                cl.login(username, password)
            except Exception as e:
                flash(f"Login failed: {e}", "error")
                return redirect(url_for("send_messages"))

            # Function to send messages
            def message_loop():
                global stop_flag
                for message in messages:
                    if stop_flag:
                        break
                    try:
                        cl.direct_send(message, thread_ids=[group_id])
                        flash(f"Sent message: {message}", "success")
                    except Exception as e:
                        flash(f"Failed to send message: {message}. Error: {e}", "error")
                    time.sleep(delay)

                if not stop_flag:
                    flash("All messages sent successfully!", "success")

            # Run message sending in a thread
            threading.Thread(target=message_loop).start()

            flash("Messages are being sent in the background!", "info")
            return redirect(url_for("send_messages"))

        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for("send_messages"))

    return render_template_string(HTML_TEMPLATE)

@app.route("/stop", methods=["POST"])
def stop_sending():
    global stop_flag
    stop_flag = True
    flash("Message sending process stopped!", "info")
    return redirect(url_for("send_messages"))

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
            
