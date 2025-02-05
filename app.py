from flask import Flask, render_template, request, redirect, url_for
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os

app = Flask(__name__)

# Path to chromedriver
CHROME_DRIVER_PATH = 'path/to/chromedriver'

def send_message(username, password, thread_id, message):
    # Setup Selenium WebDriver with options
    options = Options()
    options.headless = False  # Set to True if you want to run the browser in headless mode (no GUI)
    
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options)
    
    try:
        driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(3)  # Wait for page to load
        
        # Log in to Instagram
        username_input = driver.find_element_by_name('username')
        password_input = driver.find_element_by_name('password')
        
        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        
        time.sleep(5)  # Wait for login
        
        # Go to the thread
        driver.get(f'https://www.instagram.com/direct/inbox/{thread_id}/')
        time.sleep(3)  # Wait for thread to load
        
        # Find the message input field and send the message
        message_input = driver.find_element_by_tag_name('textarea')
        message_input.send_keys(message)
        message_input.send_keys(Keys.RETURN)
        
        time.sleep(2)  # Wait for the message to send

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

@app.route('/')
def index():
    return '''
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Instagram Message Sender</title>
        </head>
        <body>
            <h1>Instagram Message Sender</h1>
            <form action="/send_message" method="post" enctype="multipart/form-data">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required><br><br>
                
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required><br><br>
                
                <label for="thread_id">Thread ID:</label>
                <input type="text" id="thread_id" name="thread_id" required><br><br>
                
                <label for="message_file">Message File:</label>
                <input type="file" id="message_file" name="message_file" accept=".txt" required><br><br>
                
                <label for="delay">Delay (seconds):</label>
                <input type="number" id="delay" name="delay" min="1" required><br><br>
                
                <button type="submit">Send Message</button>
            </form>
        </body>
        </html>
    '''

@app.route('/send_message', methods=['POST'])
def handle_message():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        thread_id = request.form['thread_id']
        
        # Read message from the uploaded file
        message_file = request.files['message_file']
        message = message_file.read().decode('utf-8')
        
        # Send message with a delay
        delay = int(request.form['delay'])
        time.sleep(delay)
        
        send_message(username, password, thread_id, message)
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
