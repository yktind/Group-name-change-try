from flask import Flask, request, redirect, url_for, flash, get_flashed_messages
from instagrapi import Client
from markupsafe import escape

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Session management के लिए

PORT = 5000

# Instagram client instance
cl = Client()

def html_template(body):
    # बेसिक HTML template जिससे हर response बनेगा
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Instagram Group Name Changer</title>
        <style>
            body {{
                background: #111;
                font-family: Arial, sans-serif;
                color: white;
                text-align: center;
                padding-top: 100px;
            }}
            .container {{
                background-color: rgba(0, 0, 0, 0.7);
                padding: 30px;
                border-radius: 15px;
                width: 400px;
                margin: auto;
            }}
            input {{
                width: 90%;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                border: none;
            }}
            button {{
                padding: 10px 20px;
                background: #ff5e62;
                border: none;
                border-radius: 5px;
                color: white;
                font-size: 16px;
                cursor: pointer;
            }}
            .alert {{
                padding: 10px;
                margin: 10px auto;
                width: 80%;
                border-radius: 5px;
            }}
            .success {{ background-color: #28a745; }}
            .danger {{ background-color: #dc3545; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Instagram Group Chat Name Changer</h2>
            {body}
        </div>
    </body>
    </html>
    """

def get_flash_html():
    # Flash messages को HTML alert के रूप में तैयार करें
    messages = get_flashed_messages(with_categories=True)
    alerts = ""
    for category, message in messages:
        alerts += f'<div class="alert {escape(category)}">{escape(message)}</div>'
    return alerts

@app.route('/', methods=['GET', 'POST'])
def home():
    flash_html = get_flash_html()

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        thread_id = request.form.get('thread_id', '').strip()
        new_name = request.form.get('new_name', '').strip()

        if not all([username, password, thread_id, new_name]):
            flash("Please fill in all fields.", "danger")
            return redirect(url_for('home'))

        try:
            # Login to Instagram
            cl.login(username, password)

            # Change group chat name
            cl.direct_thread_rename(thread_id, new_name)

            flash("Group chat name changed successfully!", "success")
            return redirect(url_for('home'))
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
            return redirect(url_for('home'))

    form_html = f"""
        {flash_html}
        <form method="POST">
            <input type="text" name="username" placeholder="Instagram Username" required><br>
            <input type="password" name="password" placeholder="Instagram Password" required><br>
            <input type="text" name="thread_id" placeholder="Group Chat Thread ID" required><br>
            <input type="text" name="new_name" placeholder="New Group Chat Name" required><br>
            <button type="submit">Change Name</button>
        </form>
    """
    return html_template(form_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
  
