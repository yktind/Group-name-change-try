# app.py
from flask import Flask, render_template_string, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # फॉर्म की security के लिए

# HTML template (inline)
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Group Chat Name Changer</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        input, button { padding: 10px; margin: 5px 0; width: 100%%; }
        form { max-width: 400px; margin: auto; }
        .message { color: green; }
    </style>
</head>
<body>
    <h2>Group Chat Name Changer</h2>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul class=message>
        {% for message in messages %}
          <li>{{ message }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    <form method="POST">
        <label>Group Chat ID:</label><br>
        <input type="text" name="group_id" required><br>
        <label>New Group Name:</label><br>
        <input type="text" name="new_name" required><br>
        <button type="submit">Change Name</button>
    </form>
</body>
</html>
"""

# Dummy API function — यहाँ अपनी Private API logic जोड़ें
def change_group_chat_name(group_id, new_name):
    # Example: आप यहाँ Instagram API या कोई custom API call कर सकते हैं
    print(f"[DEBUG] Changing group ID {group_id} name to '{new_name}'")
    # यहाँ मान लेते हैं कि हमेशा success होता है
    return True

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        group_id = request.form['group_id']
        new_name = request.form['new_name']
        success = change_group_chat_name(group_id, new_name)
        if success:
            flash(f"Group chat '{group_id}' का नाम सफलतापूर्वक '{new_name}' में बदला गया।")
        else:
            flash("नाम बदलने में समस्या आई। कृपया पुनः प्रयास करें।")
        return redirect(url_for('home'))
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
