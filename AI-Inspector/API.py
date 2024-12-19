from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from model import model
import os

app = Flask(__name__)

# Set the upload folder
UPLOAD_FOLDER = './files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/ai', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template('index.html')

    if request.method == "POST":
        print('AI POST called')

    desc = request.form.get("desc")
    
    file = request.files.get("file")

    # Checking if the file is a python file
    if file.filename[-2:] == 'py':
        name = file.filename.split('.')[0]
        file.filename = name + '.txt'
    
    principles = request.form.getlist("principles")

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        response = model(file_path, desc, principles)

        return render_template('index.html',answer=response,error=True if response==None else False)
    
    return jsonify("Model response error")


def start_app():
    app.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == '__main__':
    start_app()
