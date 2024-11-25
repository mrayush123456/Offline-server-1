from flask import Flask, request, render_template, redirect, url_for, flash
import os
import time
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.debug = True

# Folder to store uploaded files temporarily
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Instagram Messaging Bot</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background-color: #f8f9fa;
      font-family: Arial, sans-serif;
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
    <h1 class="text-center">Instagram Messaging Bot</h1>
    <form action="/" method="POST" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="username" class="form-label">Instagram Username:</label>
        <input type="text" class="form-control" id="username" name="username" required>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Instagram Password:</label>
        <input type="password" class="form-control" id="password" name="password" required>
      </div>
      <div class="mb-3">
        <label for="target_group" class="form-label">Target Chat Group or Inbox:</label>
        <input type="text" class="form-control" id="target_group" name="target_group" required>
      </div>
      <div class="mb-3">
        <label for="haters_name" class="form-label">Hater's Name:</label>
        <input type="text" class="form-control" id="haters_name" name="haters_name" required>
      </div>
      <div class="mb-3">
        <label for="txt_file" class="form-label">Message File (.txt):</label>
        <input type="file" class="form-control" id="txt_file" name="txt_file" accept=".txt" required>
      </div>
      <div class="mb-3">
        <label for="delay" class="form-label">Delay Between Messages (in seconds):</label>
        <input type="number" class="form-control" id="delay" name="delay" min="1" required>
      </div>
      <button type="submit" class="btn btn-primary w-100">Send Messages</button>
    </form>
  </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        target_group = request.form.get('target_group')
        haters_name = request.form.get('haters_name')
        delay = int(request.form.get('delay'))
        txt_file = request.files['txt_file']

        # Save the uploaded file securely
        unique_filename = f"{uuid.uuid4()}.txt"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        txt_file.save(file_path)

        # Read the messages from the file
        try:
            with open(file_path, 'r') as file:
                messages = file.read().splitlines()
        except Exception as e:
            flash(f"Error reading the file: {e}", "danger")
            return redirect(url_for('home'))

        # Mock sending messages
        try:
            for message in messages:
                full_message = f"{haters_name}: {message}"
                print(f"Sending to {target_group}: {full_message}")
                time.sleep(delay)
        except Exception as e:
            flash(f"Error sending messages: {e}", "danger")
            return redirect(url_for('home'))
        finally:
            # Clean up uploaded file
            os.remove(file_path)

        flash(f"Messages successfully sent to {target_group}.", "success")
        return redirect(url_for('home'))

    return HTML_TEMPLATE


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

 
