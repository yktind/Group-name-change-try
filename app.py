from flask import Flask, request, render_template
from instabot import Bot

app = Flask(__name__)

@app.route("/")
def index():
    return '''
        <h2>Instagram Group Chat Automation</h2>
        <form action="/send_message" method="post">
            <label for="username">Instagram Username:</label><br>
            <input type="text" id="username" name="username" required><br><br>

            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password" required><br><br>

            <label for="group_id">Group Chat ID:</label><br>
            <input type="text" id="group_id" name="group_id" required><br><br>

            <label for="message">Message:</label><br>
            <textarea id="message" name="message" rows="4" cols="50" required></textarea><br><br>

            <button type="submit">Send Message</button>
        </form>
    '''

@app.route("/send_message", methods=["POST"])
def send_message():
    username = request.form["username"]
    password = request.form["password"]
    group_id = request.form["group_id"]
    message = request.form["message"]

    bot = Bot()
    bot.login(username=username, password=password)

    try:
        bot.send_message(message, [group_id])
        return "Message sent successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Use host='0.0.0.0' to make the server accessible externally
    # Specify port 8080 for compatibility with most hosting services
    app.run(host="0.0.0.0", port=8080, debug=True)
    
