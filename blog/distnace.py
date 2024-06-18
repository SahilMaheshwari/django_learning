import requests
import environ
env = environ.Env()
environ.Env.read_env()
api_key = env("DISTANCE_API")

def distance(origins, destinations):
    global api_key

    url = "https://api-v2.distancematrix.ai/maps/api/distancematrix/json"
    origins = "51.4822656,-0.1933769"
    destinations = "51.4994794,-0.1269979"

    # Create the query parameters
    params = {
        "origins": origins,
        "destinations": destinations,
        "key": api_key
    }

    # Make the GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        print("IT RAN")
        data = response.json()
        return data
    else:
        return f"Error: {response.status_code}"
