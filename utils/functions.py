
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "get the current weather in a given location",
            "parameters" : {
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
        },
    }
]

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

