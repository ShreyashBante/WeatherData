import os
import requests
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

def test_weather_api():
    api_key = os.getenv('WEATHER_API_KEY')
    # London coordinates
    lat = 51.5074
    lon = -0.1278
    
    # API endpoint
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        print("API Test Successful!")
        print("Current weather in London:")
        print(f"Temperature: {data['main']['temp']}°C")
        print(f"Humidity: {data['main']['humidity']}%")
        print(f"Description: {data['weather'][0]['description']}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error accessing the API: {e}")

if __name__ == "__main__":
    test_weather_api()