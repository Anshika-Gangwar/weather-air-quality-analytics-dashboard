import requests
import pandas as pd 

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 28.6139,
    "longitude": 77.2090,
    "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
    "timezone": "Asia/Kolkata"
}

response = requests.get(url, params=params)

data = response.json()
current = data["current"]

weather_record = {
    "city": "Delhi",
    "temperature": current["temperature_2m"],
    "humidity": current["relative_humidity_2m"],
    "precipitation": current["precipitation"],
    "wind_speed": current["wind_speed_10m"]
}

df = pd.DataFrame([weather_record])

print(df)

df.to_csv("data/raw/weather_data.csv", index=False)

print("Weather data saved successfully!")