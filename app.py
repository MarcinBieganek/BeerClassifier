
from flask import Flask, request, render_template, jsonify, make_response


app = Flask(__name__)

@app.route('/get-beer-classification', methods=['GET', 'POST'])
def get_beer_classification():
    return make_response(jsonify({'message': 'You will be able to get beer classification here!'}), 200)

if __name__ == '__main__':
    app.run(debug=True)