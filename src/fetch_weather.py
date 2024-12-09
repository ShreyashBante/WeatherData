# fetch_weather_maharashtra.py

import os
import requests 
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fetch_weather_data(city):
    api_key = os.getenv('WEATHER_API_KEY')
    # API endpoint for the specified city
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        print(f"Weather data for {city}:")
        print(f"Temperature: {data['main']['temp']}°C")
        print(f"Humidity: {data['main']['humidity']}%")
        print(f"Description: {data['weather'][0]['description']}")
        
        # Return the relevant data
        return {
            'city': city,
            'latitude': data['coord']['lat'],
            'longitude': data['coord']['lon'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description']
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error accessing the API: {e}")
        return None

def insert_weather_data(weather_data):
    connection = None  # Initialize connection to None
    try:
        # Connect to PostgreSQL
        connection = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT'))  # Convert port to integer
        )
        cursor = connection.cursor()
        
        # Insert data into the weather table
        insert_query = """
        INSERT INTO Weather (city, latitude, longitude, temperature, humidity, description, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, DEFAULT);
        """
        cursor.execute(insert_query, (
            weather_data['city'],
            weather_data['latitude'],
            weather_data['longitude'],
            weather_data['temperature'],
            weather_data['humidity'],
            weather_data['description']
        ))
        
        connection.commit()
        print(f"Data for {weather_data['city']} inserted successfully.")
        
    except Exception as e:
        print(f"Error inserting data into PostgreSQL: {e}")
    finally:
        if connection:  # Check if connection was established
            cursor.close()
            connection.close()

if __name__ == "__main__":
    cities = ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"]  # List of cities in Maharashtra
    for city in cities:
        weather_data = fetch_weather_data(city)
        if weather_data:
            insert_weather_data(weather_data)