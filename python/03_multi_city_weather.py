import requests
import pandas as pd


cities = {
    "Delhi": {
        "latitude": 28.6139,
        "longitude": 77.2090
    },
    "Mumbai": {
        "latitude": 19.0760,
        "longitude": 72.8777
    },
    "Bengaluru": {
        "latitude": 12.9716,
        "longitude": 77.5946
    },
    "Hyderabad": {
        "latitude": 17.3850,
        "longitude": 78.4867
    },
    "Chennai": {
        "latitude": 13.0827,
        "longitude": 80.2707
    },
    "Kolkata": {
        "latitude": 22.5726,
        "longitude": 88.3639
    },
    "Pune": {
        "latitude": 18.5204,
        "longitude": 73.8567
    },
    "Jaipur": {
        "latitude": 26.9124,
        "longitude": 75.7873
    },
    "Lucknow": {
        "latitude": 26.8467,
        "longitude": 80.9462
    },
    "Ahmedabad": {
        "latitude": 23.0225,
        "longitude": 72.5714
    }
}


weather_records = []


for city, coordinates in cities.items():

    print(f"Fetching weather data for {city}...")

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(url, params=params)

    data = response.json()

    current = data["current"]

    weather_record = {
        "city": city,
        "date": current["time"],
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "precipitation": current["precipitation"],
        "wind_speed": current["wind_speed_10m"]
    }

    weather_records.append(weather_record)


df = pd.DataFrame(weather_records)


print("\nWeather Data:")
print(df)


df.to_csv("data/raw/weather_data.csv", index=False)

print("\nWeather data saved successfully!")