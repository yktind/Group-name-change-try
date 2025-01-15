from flask import Flask, request, render_template, redirect, url_for
from instagrapi import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time

app = Flask(__name__)

# Selenium WebDriver Path (Replace with your ChromeDriver or equivalent)
WEBDRIVER_PATH = "path_to_chromedriver"  # Example: "/usr/local/bin/chromedriver"

@app.route('/')
def index():
    return '''
        <html>
        <head>
            <title>Instagram Automation</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }
                .container {
                    max-width: 500px;
                    margin: 50px auto;
                    background: #fff;
                    padding: 20px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                input, button, label {
                    display: block;
                    width: 100%;
                    margin-bottom: 10px;
                }
                button {
                    background-color: #007BFF;
                    color: #fff;
                    border: none;
                    padding: 10px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Instagram Automation</h2>
                <form action="/" method="post" enctype="multipart/form-data">
                    <label for="username">Instagram Username:</label>
                    <input type="text" id="username" name="username" required>
                    
                    <label for="password">Instagram Password:</label>
                    <input type="password" id="password" name="password" required>
                    
                    <label for="groupId">Target Group Chat ID:</label>
                    <input type="text" id="groupId" name="groupId" required>
                    
                    <label for="txtFile">Select Message File (TXT):</label>
                    <input type="file" id="txtFile" name="txtFile" accept=".txt" required>
                    
                    <label for="delay">Message Delay (Seconds):</label>
                    <input type="number" id="delay" name="delay" value="5" required>
                    
                    <button type="submit">Submit</button>
                </form>
            </div>
        </body>
        </html>
    '''

@app.route('/', methods=['POST'])
def automate_instagram():
    username = request.form.get('username')
    password = request.form.get('password')
    group_id = request.form.get('groupId')
    delay = int(request.form.get('delay'))
    
    # Get the uploaded file
    txt_file = request.files['txtFile']
    messages = txt_file.read().decode().splitlines()
    
    try:
        # Log in to Instagram using instagrapi
        cl = Client()
        cl.login(username, password)
        print("Logged in successfully.")
        
        # Send messages to the target group chat
        for message in messages:
            cl.direct_send(message, group_id)
            print(f"Sent message: {message}")
            time.sleep(delay)
        
        return "<h2>Messages sent successfully!</h2>"
    
    except Exception as e:
        print("An error occurred:", e)
        return f"<h2>Error: {e}</h2>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
