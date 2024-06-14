import os
import yaml
from flask import Flask, request, render_template, jsonify, make_response
from werkzeug.utils import secure_filename
import requests
import base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)

def load_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))  
    config_path = os.path.join(base_dir, 'config.yaml')
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: The file 'config.yaml' was not found in {base_dir}. Please check the file location.")
        exit(1) 

config = load_config()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in config['upload']['allowed_extensions']

def read_image(file_name):
    image = Image.open(file_name)
    buffered = BytesIO()

    image.save(buffered, quality=100, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    img_str = img_str.decode("ascii")

    return img_str

def classify_image(image):
    project_id = config['beer-classification-api']['project_id']
    model_version = config['beer-classification-api']['model_version']
    api_key = config['beer-classification-api']['api_key']

    res = requests.post(
        f"https://detect.roboflow.com/{project_id}/{model_version}?api_key={api_key}",
        data=image,
        headers={"Content-Type": "application/json"},
    )

    return res.json()

@app.route('/get-beer-classification', methods=['GET', 'POST'])
def get_beer_classification():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return make_response(jsonify({'error': 'No file in POST request'}), 400)  # HTTP 400 Bad Request
        
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return make_response(jsonify({'error': 'No file selected'}), 400)  # HTTP 400 Bad Request

        if not allowed_file(file.filename):
            return make_response(jsonify({'error': 'Uploaded file with not allowed extension'}), 400)  # HTTP 400 Bad Request
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(config['upload']['folder'], filename)
            file.save(filepath)

            image = read_image(filepath)
            classication_result = classify_image(image)

            if config['upload']['delete_files_after']:
                os.remove(filepath)

            return make_response(jsonify(classication_result), 200)  # HTTP 200 OK
    # GET request response
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)