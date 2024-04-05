#!/usr/bin/env python

from pprint import pprint as pp
from flask import Flask, flash, redirect, render_template, request, url_for
from weather import query_api

app = Flask(__name__)

@app.route('/')
def index():
    print('index')
    return render_template('./templates/weather.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    data = []
    error = None
    if request.method == 'POST':
        city_name = request.form.get('user_input')
        resp, location_details = query_api(city_name)
        weather_icon = location_details["weather"][0]["icon"]
        pp(resp)
        if resp:
            data.append(resp)
        if len(data) != 2: 
            error = 'Bad Response from Weather API'
    return render_template('result.html', data=data, weather_icon=weather_icon, error=error)

if __name__ == '__main__':
    app.run(debug=True)
