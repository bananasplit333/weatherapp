#!/usr/bin/env python

from pprint import pprint as pp
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from utils import kickoff
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    print('index')
    return 

@app.route('/result', methods=['POST'])
def result():
   print("POST")
   try: 
    data = request.get_data().decode('utf-8')
    print(f'DATA : {data}')
    result = kickoff(data)
    if result:
        return result
    else:
        return jsonify({"error": "Error processing city"}), 400
   except Exception as e:
      return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
