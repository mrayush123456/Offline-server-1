from flask import Flask, request, render_template_string
from instagrapi import Client
import time

app = Flask(__name__)

# HTML template for the webpage
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
            background-color: blue;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: pink;
        }
        .container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            max-width: 400px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: pink;
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-weight: bold;
            margin: 10px 0 5px;
            color: pink;
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
            background-color: yellow;
        }
        input:focus, select:focus, button:focus {
            outline: none;
            border-color: pink;
            box-shadow: 0 0 5px rgba(255, 105, 180, 0.5);
        }
        button {
            background-color: pink;
            color: blue;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #ff69b4;
        }
        .message {
            color: red;
            font-size: 14px;
            text-align: center;
        }
        .success {
            color: green;
            font-size: 14px;
            text-align: center;
        }
        .info {
            font-size: 12px;
            color: #777;
            margin-bottom: -10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Automation</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="username">Instagram Username:</label>
            <input type="text" id="username" name="username" placeholder="Enter your username" required>

            <label for="password">Instagram Password:</label>
            <input type="password" id="password" name="password" placeholder="Enter your password" required>

            <label for="choice">Send To:</label>
            <select id="choice" name="choice" required>
                <option value="inbox">Inbox</option>
                <option value="group">Group</option>
            </select>

            <label for="target_username">Target Username (for Inbox):</label>
            <input type="text" id="target_username" name="target_username" placeholder="Enter target username">

            <label for="thread_id">Thread ID (for Group):</label>
            <input type="text" id="thread_id" name="thread_id" placeholder="Enter group thread ID">

            <label for="haters_name">Haters Name:</label>
            <input type="text" id="haters_name" name="haters_name" placeholder="Enter hater's name" required>

            <label for="message_file">Message File:</label>
            <input type="file" id="message_file" name="message_file" required>
            <p class="info">Upload a file containing messages, one per line.</p>

            <label for="delay">Delay (seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay in seconds" required>

            <button type="submit">Send Messages</button>
        </form>
    </div>
</body>
</html>
'''

# Instagram login function
def instagram_login(username, password):
    try:
        cl = Client()
        cl.login(username, password)
        print("[SUCCESS] Logged into Instagram!")
        return cl
    except Exception as e:
        print(f"[ERROR] Login failed: {e}")
        return None

# Send message function
def send_messages(cl, choice, target_username, thread_id, messages, delay):
    try:
        if choice == "inbox":
            user_id = cl.user_id_from_username(target_username)
            for message in messages:
                cl.direct_send(message, [user_id])
                print(f"[SUCCESS] Sent to {target_username}: {message}")
                time.sleep(delay)
        elif choice == "group":
            for message in messages:
                cl.direct_send(message, thread_id=thread_id)
                print(f"[SUCCESS] Sent to group {thread_id}: {message}")
                time.sleep(delay)
    except Exception as e:
        print(f"[ERROR] Failed to send message: {e}")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        choice = request.form.get("choice")
        target_username = request.form.get("target_username")
        thread_id = request.form.get("thread_id")
        delay = int(request.form.get("delay"))
        haters_name = request.form.get("haters_name")
        message_file = request.files["message_file"]

        # Read messages from file
        try:
            messages = [f"{haters_name} {line}" for line in message_file.read().decode("utf-8").splitlines()]
        except Exception as e:
            return f"<p>Error reading file: {e}</p>"

        # Log into Instagram
        cl = instagram_login(username, password)
        if not cl:
            return "<p>Login failed. Check your credentials and try again.</p>"

        # Send messages
        send_messages(cl, choice, target_username, thread_id, messages, delay)
        return "<p>Messages sent successfully!</p>"

    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(debug=True)
    
