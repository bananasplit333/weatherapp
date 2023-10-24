#!/usr/bin/env python

from pprint import pprint as pp
from flask import Flask, flash, redirect, render_template, request, url_for
from weather import query_api

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('weather.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    data = []
    error = None
    if request.method == 'POST':
        city_name = request.form.get('user_input')
        resp = query_api(city_name)
        img_string = resp["weather"][0]["icon"]
        print(img-img_string)
        pp(resp)
        if resp:
            data.append(resp)
        if len(data) != 2: 
            error = 'Bad Response from Weather API'
    return render_template('result.html', data=data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
