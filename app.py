from flask import Flask, request, render_template, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Flask route for the homepage
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Instagram Automation</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 0; }
            .container { max-width: 600px; margin: 50px auto; padding: 20px; background: #fff; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
            h2 { text-align: center; color: #333; }
            form { display: flex; flex-direction: column; gap: 15px; }
            input, button { padding: 10px; border-radius: 5px; border: 1px solid #ddd; }
            button { background-color: #007BFF; color: white; cursor: pointer; }
            button:hover { background-color: #0056b3; }
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

                <label for="group_id">Target Group Chat ID:</label>
                <input type="text" id="group_id" name="group_id" required>

                <label for="txtFile">Select Text File with Messages:</label>
                <input type="file" id="txtFile" name="txtFile" accept=".txt" required>

                <label for="delay">Delay (seconds) between messages:</label>
                <input type="number" id="delay" name="delay" value="5" required>

                <button type="submit">Submit</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def send_instagram_messages():
    # Get form data
    username = request.form['username']
    password = request.form['password']
    group_id = request.form['group_id']
    delay = int(request.form['delay'])

    # Save the uploaded file
    file = request.files['txtFile']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Read messages from the file
    with open(filepath, 'r') as f:
        messages = f.readlines()

    # Selenium WebDriver setup
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    try:
        # Log in to Instagram
        driver.get('https://www.instagram.com/accounts/login/')
        time.sleep(5)
        driver.find_element(By.NAME, 'username').send_keys(username)
        driver.find_element(By.NAME, 'password').send_keys(password)
        driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
        time.sleep(5)

        # Navigate to the group chat
        driver.get(f'https://www.instagram.com/direct/t/{group_id}/')
        time.sleep(5)

        # Send messages
        for message in messages:
            message_box = driver.find_element(By.XPATH, '//textarea[@placeholder="Message..."]')
            message_box.send_keys(message.strip())
            message_box.send_keys(Keys.RETURN)
            time.sleep(delay)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
