import os
import yaml
from flask import Flask, request, render_template, jsonify, make_response


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

@app.route('/get-beer-classification', methods=['GET', 'POST'])
def get_beer_classification():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)