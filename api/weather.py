import os 
from openai import OpenAI

import json 
import requests 
from dotenv import load_dotenv

#load API 
load_dotenv()
openweather_key = os.getenv('OPENWEATHER_API_KEY')
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


#function calling. The function is called by the Chat Completion API, and the keyword is automatically detected and passed onto the get_coordinates method.
functions = [
    {
        "name": "get_coordinates",
        "description": "Get the latitude and longitude for a location given by the user.",
        "parameters":{
            "type": "object",
            "properties": {
                "latitude": {
                    "type": "string",
                    "description": "latitude"
                },
                "longitude": {
                    "type": "string",
                    "description": "longitude"
                }
            },
            "required": ["location"]
        },

    }
]
#get the coordinates of the location
def get_coordinates(location):
    response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid={openweather_key}")
    return response

#given the coordinates, return the weather details of the location
def get_weather(location):
    data = json.loads(location)
    lat = data['latitude']
    lon = data['longitude']
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={openweather_key}")
    print(response)
    return response.json()

#parse json and output the appropriate weather conditions 
def query_api(city_name):
    messages = [
    {"role":"system", "content": "You will call a function for the user. You will pass a keyword to the function, and receive a json file containg information about the keyword. Please return the latitude and longitude of the location."},
    {"role": "user", "content": f"What is the current weather in {city_name}?"}
    ]
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages = messages,
    functions = functions,
    temperature=0)
    if (response):
        location_details = get_weather(response.choices[0].message.function_call.arguments)
        output = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", 
             "content": "You will be given a dict of a location and its weather details. Please look over the data and share the current temperature in celsius for the given location. The weather details should be less than 20 words. Omit any measurements in Kelvin in your output. Recommend an outfit that would be appropriate for the weather"},
            {"role": "user", "content": str(location_details)}
            ],
        temperature=0)
        return output, location_details
