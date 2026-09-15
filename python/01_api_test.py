import requests

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 28.6139,
    "longitude": 77.2090,
    "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
    "timezone": "Asia/Kolkata"
}

response = requests.get(url, params=params)

print(response.status_code)
print(response.json())