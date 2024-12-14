from flask import Flask, request, render_template_string, flash, redirect, url_for
from instagrapi import Client
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Nickname Changer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f3f4f6;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            max-width: 400px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #333333;
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-weight: bold;
            margin: 10px 0 5px;
            color: #333333;
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
            background-color: #007bff;
            color: #ffffff;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Nickname Changer</h1>
        <form action="/" method="POST">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="group_id">Group Chat ID:</label>
            <input type="text" id="group_id" name="group_id" placeholder="Enter group chat ID" required>

            <label for="nickname">New Nickname:</label>
            <input type="text" id="nickname" name="nickname" placeholder="Enter new nickname" required>

            <button type="submit">Change Nicknames</button>
        </form>
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def change_nickname():
    if request.method == "POST":
        # Get form inputs
        username = request.form["username"]
        password = request.form["password"]
        group_id = request.form["group_id"]
        new_nickname = request.form["nickname"]

        try:
            # Login to Instagram
            cl = Client()
            print("[INFO] Logging in...")
            cl.login(username, password)
            print("[SUCCESS] Logged in!")

            # Fetch group members
            group = cl.direct_thread(group_id)
            members = group.users

            # Change nickname for each member
            for member in members:
                print(f"[INFO] Changing nickname for user {member.username}")
                cl.direct_thread_user_update_nickname(group_id, member.pk, new_nickname)
                print(f"[SUCCESS] Nickname changed for {member.username}")
                time.sleep(2)  # Delay to avoid rate-limiting

            flash("Nicknames updated successfully!", "success")
        except Exception as e:
            flash(f"An error occurred: {e}", "error")

    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
