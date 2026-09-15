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


all_weather_data = []


for city, coordinates in cities.items():

    print(f"Fetching historical data for {city}...")

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "start_date": "2026-08-15",
        "end_date": "2026-09-13",
        "daily": "temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum,wind_speed_10m_mean",
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(url, params=params)

    data = response.json()

    daily = data["daily"]

    for i in range(len(daily["time"])):

        weather_record = {
            "city": city,
            "date": daily["time"][i],
            "temperature": daily["temperature_2m_mean"][i],
            "humidity": daily["relative_humidity_2m_mean"][i],
            "precipitation": daily["precipitation_sum"][i],
            "wind_speed": daily["wind_speed_10m_mean"][i]
        }

        all_weather_data.append(weather_record)


df = pd.DataFrame(all_weather_data)

df["date"] = pd.to_datetime(df["date"])

print("\nHistorical weather data:")
print(df.head())

print("\nShape:")
print(df.shape)

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate city/date records:")
print(df.duplicated(subset=["city", "date"]).sum())

df.to_csv(
    "data/raw/historical_weather.csv",
    index=False
)

print("\nHistorical weather data saved successfully!")