from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

app = Flask(__name__)

# Ensure uploads directory exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Function to automate SayHi login and messaging
def send_sayhi_message(email, chat_id, message, delay):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=options)

    try:
        # Open SayHi login page
        driver.get("https://sayhi.com/login")
        time.sleep(2)

        # Enter Email
        email_input = driver.find_element(By.NAME, "email")
        email_input.send_keys(email)

        # Submit Login (Adjust based on actual site)
        email_input.send_keys(Keys.RETURN)
        time.sleep(3)

        # Navigate to target chat
        driver.get(f"https://sayhi.com/chat/{chat_id}")
        time.sleep(2)

        # Enter Message
        message_input = driver.find_element(By.NAME, "message")
        message_input.send_keys(message)
        message_input.send_keys(Keys.RETURN)

        # Introduce delay
        time.sleep(delay)

        print("Message sent successfully!")

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]
        chat_id = request.form["chat_id"]
        message = request.form["message"]
        delay = int(request.form["delay"])

        # Handle File Upload
        if "file" in request.files:
            file = request.files["file"]
            if file.filename != "":
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))

        # Run automation
        send_sayhi_message(email, chat_id, message, delay)
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>SayHi Automation</title>
    </head>
    <body>
        <h2>SayHi Automation</h2>
        <form method="POST" enctype="multipart/form-data">
            <label>Email:</label>
            <input type="email" name="email" required><br>
            <label>Chat ID:</label>
            <input type="text" name="chat_id" required><br>
            <label>Message:</label>
            <input type="text" name="message" required><br>
            <label>Select File (Optional):</label>
            <input type="file" name="file"><br>
            <label>Delay (Seconds):</label>
            <input type="number" name="delay" required><br>
            <input type="submit" value="Send Message">
        </form>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
