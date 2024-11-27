from flask import Flask, request, render_template_string
from instagrapi import Client
import time

app = Flask(__name__)

# HTML template for the web page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Automation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #1e1e2f;
            color: #fff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #2e2e3e;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            max-width: 400px;
            width: 100%;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
        }
        label {
            font-weight: bold;
            margin-top: 10px;
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            background-color: #ff5722;
            color: #fff;
            font-weight: bold;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #e64a19;
        }
        .info {
            font-size: 12px;
            color: #aaa;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Automation</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter Instagram username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter Instagram password" required>

            <label for="choice">Send To:</label>
            <select id="choice" name="choice" required>
                <option value="inbox">Inbox</option>
                <option value="group">Group</option>
            </select>

            <label for="target_username">Target Username (for Inbox):</label>
            <input type="text" id="target_username" name="target_username" placeholder="Enter target username">

            <label for="thread_id">Thread ID (for Group):</label>
            <input type="text" id="thread_id" name="thread_id" placeholder="Enter group thread ID">

            <label for="haters_name">Hater's Name:</label>
            <input type="text" id="haters_name" name="haters_name" placeholder="Enter hater's name" required>

            <label for="message_file">Message File:</label>
            <input type="file" id="message_file" name="message_file" accept=".txt" required>
            <p class="info">Upload a TXT file with one message per line.</p>

            <label for="delay">Delay (in seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay in seconds" required>

            <button type="submit">Send Messages</button>
        </form>
    </div>
</body>
</html>
'''

# Function to log in to Instagram
def instagram_login(username, password):
    try:
        client = Client()
        client.login(username, password)
        print("[SUCCESS] Logged in successfully.")
        return client
    except Exception as e:
        print(f"[ERROR] Login failed: {e}")
        return None

# Function to send messages
def send_messages(client, choice, target_username, thread_id, messages, delay):
    try:
        if choice == "inbox":
            user_id = client.user_id_from_username(target_username)
            for message in messages:
                client.direct_send(message, [user_id])
                print(f"[SUCCESS] Sent message to {target_username}: {message}")
                time.sleep(delay)
        elif choice == "group":
            for message in messages:
                client.direct_send(message, thread_id=thread_id)
                print(f"[SUCCESS] Sent message to group {thread_id}: {message}")
                time.sleep(delay)
    except Exception as e:
        print(f"[ERROR] Failed to send messages: {e}")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        choice = request.form.get("choice")
        target_username = request.form.get("target_username")
        thread_id = request.form.get("thread_id")
        haters_name = request.form.get("haters_name")
        delay = int(request.form.get("delay"))
        message_file = request.files["message_file"]

        # Read messages from the uploaded file
        try:
            messages = [f"{haters_name}: {line.strip()}" for line in message_file.read().decode("utf-8").splitlines()]
        except Exception as e:
            return f"<p>Error reading file: {e}</p>"

        # Log in to Instagram
        client = instagram_login(username, password)
        if not client:
            return "<p>Login failed. Please check your credentials and try again.</p>"

        # Send messages
        send_messages(client, choice, target_username, thread_id, messages, delay)
        return "<p>Messages sent successfully!</p>"

    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
        
