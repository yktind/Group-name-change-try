from flask import Flask, request, render_template_string
import asyncio
import threading
import os

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Script Manager</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; }
        .container { max-width: 800px; margin: auto; padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        textarea, input, button { width: 100%; margin-bottom: 10px; padding: 10px; border-radius: 5px; border: 1px solid #ccc; }
        button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
        .log { background-color: #f4f4f4; padding: 10px; border-radius: 5px; max-height: 300px; overflow-y: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h2>WhatsApp Automation</h2>
        <form method="POST" action="/">
            <label for="config">Enter Configurations (Phone Number, Interval, Target, etc.):</label>
            <textarea name="config" rows="5" placeholder="Enter configuration details here..." required></textarea>
            <button type="submit">Run Script</button>
        </form>
        <div class="log">
            <h3>Script Logs:</h3>
            <pre id="logs">{{ logs }}</pre>
        </div>
    </div>
</body>
</html>
"""

app = Flask(__name__)
logs = []  # Stores logs to display on the webpage

# Function to append logs
def add_log(message):
    global logs
    logs.append(message)
    if len(logs) > 100:
        logs = logs[-100:]  # Keep last 100 logs


# Function to run the async script
async def run_async_script(config):
    add_log("Running script with configuration:\n" + config)
    try:
        exec(open("your_async_script.js").read())  # Replace with your async JS script logic
        add_log("Script executed successfully!")
    except Exception as e:
        add_log(f"Error during script execution: {e}")


# Background thread for running the script
def run_script_in_background(config):
    asyncio.run(run_async_script(config))


@app.route("/", methods=["GET", "POST"])
def index():
    global logs
    if request.method == "POST":
        config = request.form.get("config")
        if config:
            add_log(f"Received configuration: {config}")
            thread = threading.Thread(target=run_script_in_background, args=(config,))
            thread.start()
            add_log("Script started in the background.")
        else:
            add_log("No configuration received.")
    return render_template_string(HTML_TEMPLATE, logs="\n".join(logs))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
