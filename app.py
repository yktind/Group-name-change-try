from flask import Flask, request, render_template, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Flask App
app = Flask(__name__)

# Configure ChromeDriver Path
CHROME_DRIVER_PATH = "chromedriver"  # Update with your ChromeDriver path

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
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                width: 400px;
            }
            input, button {
                width: 100%;
                padding: 10px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            button {
                background-color: #007bff;
                color: white;
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
                <input type="text" name="username" placeholder="Instagram Username" required>
                <input type="password" name="password" placeholder="Instagram Password" required>
                <input type="text" name="group_id" placeholder="Target Group Chat ID" required>
                <input type="number" name="delay" placeholder="Delay in Seconds" value="5" required>
                <input type="file" name="message_file" accept=".txt" required>
                <button type="submit">Submit</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def automate_instagram():
    # Extract form data
    username = request.form['username']
    password = request.form['password']
    group_id = request.form['group_id']
    delay = int(request.form['delay'])
    message_file = request.files['message_file']
    messages = message_file.read().decode('utf-8').splitlines()

    # Setup Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open Instagram
        driver.get("https://www.instagram.com/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        # Login
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

        # Wait for the homepage to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/direct/inbox/')]")))

        # Navigate to group chat
        driver.get(f"https://www.instagram.com/direct/t/{group_id}/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//textarea")))

        # Send messages
        for message in messages:
            textarea = driver.find_element(By.XPATH, "//textarea")
            textarea.send_keys(message)
            textarea.send_keys(Keys.RETURN)
            time.sleep(delay)  # Delay between messages

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()

    return "Messages sent successfully!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
