import requests
import pandas as pd

cities = {
    "Delhi": {"latitude": 28.6139, "longitude": 77.2090},
    "Mumbai": {"latitude": 19.0760, "longitude": 72.8777},
    "Bengaluru": {"latitude": 12.9716, "longitude": 77.5946},
    "Hyderabad": {"latitude": 17.3850, "longitude": 78.4867},
    "Chennai": {"latitude": 13.0827, "longitude": 80.2707},
    "Kolkata": {"latitude": 22.5726, "longitude": 88.3639},
    "Pune": {"latitude": 18.5204, "longitude": 73.8567},
    "Jaipur": {"latitude": 26.9124, "longitude": 75.7873},
    "Lucknow": {"latitude": 26.8467, "longitude": 80.9462},
    "Ahmedabad": {"latitude": 23.0225, "longitude": 72.5714}
}

start_date = "2026-08-15"
end_date = "2026-09-13"

all_data = []

for city, coordinates in cities.items():

    print(f"Fetching air quality data for {city}...")

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    params = {
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi",
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error for {city}: {response.status_code}")
        continue

    data = response.json()

    hourly = data["hourly"]

    city_df = pd.DataFrame({
        "city": city,
        "datetime": hourly["time"],
        "pm2_5": hourly["pm2_5"],
        "pm10": hourly["pm10"],
        "carbon_monoxide": hourly["carbon_monoxide"],
        "nitrogen_dioxide": hourly["nitrogen_dioxide"],
        "sulphur_dioxide": hourly["sulphur_dioxide"],
        "ozone": hourly["ozone"],
        "us_aqi": hourly["us_aqi"]
    })

    all_data.append(city_df)


aqi_df = pd.concat(all_data, ignore_index=True)

aqi_df["datetime"] = pd.to_datetime(aqi_df["datetime"])

# Create a date column so we can connect AQI with daily weather data
aqi_df["date"] = aqi_df["datetime"].dt.date

print("\nAir quality data:")
print(aqi_df.head())

print("\nShape:")
print(aqi_df.shape)

print("\nMissing values:")
print(aqi_df.isnull().sum())

# Save raw hourly data
aqi_df.to_csv(
    "data/raw/historical_air_quality_hourly.csv",
    index=False
)

# Create daily city-level summary
daily_aqi = (
    aqi_df
    .groupby(["city", "date"])
    .agg(
        avg_aqi=("us_aqi", "mean"),
        max_aqi=("us_aqi", "max"),
        avg_pm2_5=("pm2_5", "mean"),
        avg_pm10=("pm10", "mean"),
        avg_co=("carbon_monoxide", "mean"),
        avg_no2=("nitrogen_dioxide", "mean"),
        avg_so2=("sulphur_dioxide", "mean"),
        avg_o3=("ozone", "mean")
    )
    .reset_index()
)

daily_aqi.to_csv(
    "data/raw/historical_air_quality_daily.csv",
    index=False
)

print("\nDaily AQI data:")
print(daily_aqi.head())

print("\nDaily AQI shape:")
print(daily_aqi.shape)

print("\nHistorical air quality data saved successfully!")