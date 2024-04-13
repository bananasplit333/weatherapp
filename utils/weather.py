import json 
import os 
import requests
from dotenv import load_dotenv
from .chat_completion import groq_completion_request
from datetime import date

#get openweather api 
load_dotenv()
openweather_key = os.getenv('OPENWEATHER_API_KEY')
#get the coordinates of the location
def get_coordinates(location):
    response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=5&appid={openweather_key}")
    data= response.json()
    if data:
        coordinate_details = data[0]
        lat=coordinate_details['lat']
        lon=coordinate_details['lon']
        return lat, lon
    else:
        return None, None, 

#given the coordinates, return the weather details of the location
def get_weather(location):
    data = get_coordinates(location=location)
    print(f"DATA : {data}")
    lat = data[0]
    lon = data[1]
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={openweather_key}")
    return response.json()

def kickoff(location):
    weather_details = get_weather(location)
    icon = weather_details['weather'][0]['icon']
    feels_like = weather_details['main']['feels_like']
    temp_min = weather_details['main']['temp_min']
    temp_max = weather_details['main']['temp_max']
    curr_temp = weather_details['main']['temp']
    wind_speed = weather_details['wind']['speed']
    city_name = weather_details['name']
    curr_time = date.today()

    weather_data = {
        "icon": icon,
        "city_name": city_name,
        "current_time": str(curr_time),
        "temperatures" : {
            "current": curr_temp,
            "feels_like": feels_like,
            "min": temp_min,
            "max": temp_max,
        },
        "wind": {
            "speed": wind_speed
        }
    }

    messages = [
    {"role":"system", 
     "content":'''You will be given a json object of weather data. Please take a look at the current weather conditions and suggest an outfit for the user.
                  Please provide an introductory sentence and then recommend the articles of clothing. 
                  After that, quickly recommend one activity that they can do with the current weather conditions.
                  
                  e.g. 'It looks like it will be very sunny in Seoul today. For this kind of day, I suggest a pair of nice sandals, sunglasses, 
                  light tshirt, and shorts. I recommend going out for a swim and taking advantage of the sun today! 
                
                  Make sure your entire output is 50 words or less.
                
                '''
                },
    {"role": "user",
     "content": json.dumps(weather_data)}
    ]
    response = groq_completion_request(messages=messages, tool_choice="none")
    response_content = response.choices[0].message.content
    print(response_content)
    #combine results 
    result = {
        "weather_data": weather_data, 
        "chat_response": response_content
    }
    print(f"RESULT : {result}")
    return result

