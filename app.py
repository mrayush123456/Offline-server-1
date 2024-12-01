from flask import Flask, request, render_template
import requests
import time
import os

app = Flask(__name__)
app.debug = True

# HTML Templates
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Instagram Messaging Bot</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background-color: #f8f9fa;
    }
    .container {
      max-width: 500px;
      background-color: #fff;
      border-radius: 10px;
      padding: 20px;
      margin: 0 auto;
      margin-top: 50px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
  </style>
</head>
<body>
  <div class="container">
    <h1 class="text-center mb-4">Instagram Messaging Bot</h1>
    <form action="/" method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="username">Instagram Username:</label>
        <input type="text" class="form-control" id="username" name="username" required>
      </div>
      <div class="mb-3">
        <label for="password">Instagram Password:</label>
        <input type="password" class="form-control" id="password" name="password" required>
      </div>
      <div class="mb-3">
        <label for="targetUsername">Target Instagram Username:</label>
        <input type="text" class="form-control" id="targetUsername" name="targetUsername" required>
      </div>
      <div class="mb-3">
        <label for="hatersName">Hater's Name:</label>
        <input type="text" class="form-control" id="hatersName" name="hatersName" required>
      </div>
      <div class="mb-3">
        <label for="txtFile">Message File (.txt):</label>
        <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
      </div>
      <div class="mb-3">
        <label for="timeInterval">Time Interval (seconds):</label>
        <input type="number" class="form-control" id="timeInterval" name="timeInterval" required>
      </div>
      <button type="submit" class="btn btn-primary w-100">Submit</button>
    </form>
  </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def instagram_bot():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        target_username = request.form.get('targetUsername')
        haters_name = request.form.get('hatersName')
        time_interval = int(request.form.get('timeInterval'))
        txt_file = request.files['txtFile']

        # Save the uploaded file temporarily
        file_path = os.path.join('uploaded_messages.txt')
        txt_file.save(file_path)

        # Read messages from the file
        with open(file_path, 'r') as f:
            messages = f.read().splitlines()

        # Mock login (for demo purposes, replace with actual Instagram API calls)
        if username and password:
            print(f"Logged in as {username}")

            # Mock target user ID lookup (replace with real API call)
            print(f"Target Username: {target_username}")

            # Sending messages
            for message in messages:
                try:
                    # Replace this print with the actual API call to send messages
                    print(f"Sending to {target_username}: {haters_name} {message}")
                    time.sleep(time_interval)
                except Exception as e:
                    print(f"Error while sending message: {e}")
            
            return f"Messages successfully sent to {target_username}."
        else:
            return "Login failed. Please check your username and password.", 401

    # Render HTML form
    return HTML_TEMPLATE


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
