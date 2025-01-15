from flask import Flask, request, render_template, redirect, url_for, flash
from instagrapi import Client
import os
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
cl = Client()

# Store login sessions
sessions = {}

@app.route('/')
def index():
    return '''
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Instagram Group Chat Message Sender</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 0;
            }
            .container {
                width: 50%;
                margin: 50px auto;
                background: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .form-control {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            .btn {
                padding: 10px 15px;
                background: #007bff;
                color: #fff;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .btn:hover {
                background: #0056b3;
            }
            h3 {
                text-align: center;
                color: #333;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h3>Instagram Group Chat Message Sender</h3>
            <form action="/login" method="post">
                <input type="text" name="username" class="form-control" placeholder="Instagram Username" required>
                <input type="password" name="password" class="form-control" placeholder="Instagram Password" required>
                <button type="submit" class="btn">Login</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    try:
        cl.login(username, password)
        sessions['username'] = username
        flash("Login successful!", "success")
        return redirect(url_for('message_form'))
    except Exception as e:
        flash(f"Login failed: {str(e)}", "danger")
        return redirect(url_for('index'))

@app.route('/message', methods=['GET', 'POST'])
def message_form():
    if 'username' not in sessions:
        flash("Please login first.", "warning")
        return redirect(url_for('index'))

    if request.method == 'POST':
        target_group = request.form.get('group_id')
        delay = int(request.form.get('delay'))
        txt_file = request.files['txtFile']

        # Read messages from the file
        messages = txt_file.read().decode('utf-8').splitlines()

        try:
            for i, message in enumerate(messages):
                cl.direct_send(message, [target_group])
                flash(f"Sent message {i+1}/{len(messages)} to group {target_group}.", "info")
                time.sleep(delay)
            flash("All messages sent successfully!", "success")
        except Exception as e:
            flash(f"Error sending messages: {str(e)}", "danger")

    return '''
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Send Messages</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 0;
            }
            .container {
                width: 50%;
                margin: 50px auto;
                background: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .form-control {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            .btn {
                padding: 10px 15px;
                background: #007bff;
                color: #fff;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .btn:hover {
                background: #0056b3;
            }
            h3 {
                text-align: center;
                color: #333;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h3>Send Messages to Group Chat</h3>
            <form action="/message" method="post" enctype="multipart/form-data">
                <input type="text" name="group_id" class="form-control" placeholder="Target Group Chat ID" required>
                <input type="file" name="txtFile" class="form-control" accept=".txt" required>
                <input type="number" name="delay" class="form-control" placeholder="Delay (seconds)" required>
                <button type="submit" class="btn">Send Messages</button>
            </form>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
