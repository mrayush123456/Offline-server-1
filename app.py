import os
import time
import requests
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Facebook API URL
FB_API_URL = "https://graph.facebook.com/v16.0/me/messages"

@app.route("/", methods=["GET", "POST"])
def send_message():
    if request.method == "POST":
        # Retrieve form data
        access_token = request.form.get("accessToken")
        recipient_id = request.form.get("recipientId")
        delay = int(request.form.get("time"))
        txt_file = request.files["txtFile"]

        # Read messages from the uploaded TXT file
        messages = txt_file.read().decode().splitlines()

        # Send each message with a delay
        for message in messages:
            try:
                payload = {
                    "recipient": {"id": recipient_id},
                    "message": {"text": message}
                }
                headers = {"Authorization": f"Bearer {access_token}"}
                response = requests.post(FB_API_URL, json=payload, headers=headers)

                if response.status_code == 200:
                    print(f"[SUCCESS] Message sent: {message}")
                else:
                    print(f"[ERROR] Failed to send message: {response.text}")

                time.sleep(delay)

            except Exception as e:
                print(f"[ERROR] Exception occurred: {e}")
                time.sleep(30)

        return jsonify({"status": "Messages sent successfully!"})

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Facebook Messenger Bot</title>
    </head>
    <body>
        <h1>Send Messages to Facebook Messenger</h1>
        <form method="POST" enctype="multipart/form-data">
            <label>Page Access Token:</label>
            <input type="text" name="accessToken" required><br><br>

            <label>Recipient ID (PSID):</label>
            <input type="text" name="recipientId" required><br><br>

            <label>Message File (TXT):</label>
            <input type="file" name="txtFile" required><br><br>

            <label>Delay (seconds):</label>
            <input type="number" name="time" required><br><br>

            <button type="submit">Send Messages</button>
        </form>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
