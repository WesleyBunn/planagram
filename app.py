from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os
from werkzeug.utils import secure_filename  # Import secure_filename function

app = Flask(__name__)

# Define the path to the uploads folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("input_word.html")

@app.route("/process", methods=["POST"])
def process_word():
    username = request.form["username"]
    password = request.form["password"]
    caption = request.form["caption"]
    scheduleTime = request.form["scheduleTime"]

    # Check if the post request has the file part
    if 'image' not in request.files:
        return "No file part"
    file = request.files['image']
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return "No selected file"
    # If the file exists and is allowed
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)  # Save the file to the uploads folder

    subprocess.run(["python", "file.py", username, password, caption, scheduleTime])
    return redirect(url_for("index"))

print("Server is running at http://localhost:5000")  # Print the URL before starting the server

if __name__ == "__main__":
    app.run(debug=True)
