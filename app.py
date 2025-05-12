from flask import Flask, render_template_string, request, redirect, url_for, flash
from instagrapi import Client

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Flask flash message के लिए

# HTML template (simple form)
template = '''
<!doctype html>
<title>Instagram Group Chat Name Changer</title>
<h2>Instagram Group Chat Name Changer</h2>
<form method=post>
  <label>Instagram Username:</label><br>
  <input type=text name=username required><br><br>

  <label>Instagram Password:</label><br>
  <input type=password name=password required><br><br>

  <label>Target Group Chat (Thread ID):</label><br>
  <input type=text name=thread_id required><br><br>

  <label>New Group Name:</label><br>
  <input type=text name=new_name required><br><br>

  <button type=submit>Change Group Name</button>
</form>

{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul>
    {% for message in messages %}
      <li><strong>{{ message }}</strong></li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        thread_id = request.form['thread_id']
        new_name = request.form['new_name']

        cl = Client()

        try:
            cl.login(username, password)
        except Exception as e:
            flash(f'Login failed: {e}')
            return redirect(url_for('index'))

        try:
            cl.direct_thread_update_title(thread_id, new_name)
            flash(f'Success! Group name changed to: {new_name}')
        except Exception as e:
            flash(f'Failed to change group name: {e}')

        cl.logout()
        return redirect(url_for('index'))

    return render_template_string(template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
