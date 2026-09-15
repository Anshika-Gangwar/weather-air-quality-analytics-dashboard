import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote_plus

load_dotenv()

user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
port = os.getenv("MYSQL_PORT")
database = os.getenv("MYSQL_DATABASE")

encoded_password = quote_plus(password)
engine = create_engine(
    f"mysql+pymysql://{user}:{encoded_password}@{host}:{port}/{database}"
)

query = """
SELECT
    w.city,
    w.date,
    w.temperature,
    w.humidity,
    w.precipitation,
    w.wind_speed,
    a.avg_aqi,
    a.max_aqi,
    a.avg_pm2_5,
    a.avg_pm10,
    a.avg_no2,
    a.avg_so2,
    a.avg_o3
FROM weather_data AS w
INNER JOIN air_quality AS a
    ON w.city = a.city
    AND w.date = a.date
"""

df = pd.read_sql(query, engine)

print("Data loaded successfully!")
print("Shape:", df.shape)

# Average AQI by city
aqi_by_city = (
    df.groupby("city")["avg_aqi"]
    .mean()
    .sort_values(ascending=False)
)

# Create visualization
plt.figure(figsize=(10, 6))

aqi_by_city.plot(kind="bar")

plt.title("Average AQI by City")
plt.xlabel("City")
plt.ylabel("Average AQI")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

# Average temperature by city
temperature_by_city = (
    df.groupby("city")["temperature"]
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))

temperature_by_city.plot(kind="bar")

plt.title("Average Temperature by City")
plt.xlabel("City")
plt.ylabel("Average Temperature (°C)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

# Average PM2.5 and PM10 by city
pollution_by_city = (
    df.groupby("city")[["avg_pm2_5", "avg_pm10"]]
    .mean()
    .sort_values("avg_pm2_5", ascending=False)
)

plt.figure(figsize=(10, 6))

pollution_by_city.plot(kind="bar")

plt.title("Average PM2.5 and PM10 by City")
plt.xlabel("City")
plt.ylabel("Concentration (µg/m³)")
plt.xticks(rotation=45)

plt.legend(
    title="Pollutant",
    labels=["PM2.5", "PM10"]
)

plt.tight_layout()
plt.show()

# Daily average AQI trend
daily_aqi = (
    df.groupby("date")["avg_aqi"]
    .mean()
    .sort_index()
)

plt.figure(figsize=(12, 6))

daily_aqi.plot(kind="line", marker="o")

plt.title("Average AQI Trend Over 30 Days")
plt.xlabel("Date")
plt.ylabel("Average AQI")
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()

# Temperature vs AQI
plt.figure(figsize=(10, 6))

plt.scatter(
    df["temperature"],
    df["avg_aqi"],
    alpha=0.6
)

plt.title("Temperature vs AQI")
plt.xlabel("Temperature (°C)")
plt.ylabel("Average AQI")
plt.grid(True)

plt.tight_layout()
plt.show()

# Pollutant correlation with AQI

pollutant_correlations = (
    df[
        ["avg_pm2_5", "avg_pm10", "avg_no2", "avg_so2", "avg_o3", "avg_aqi"]
    ]
    .corr()["avg_aqi"]
    .drop("avg_aqi")
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
pollutant_correlations.plot(kind="bar")

plt.title("Pollutant Correlation with AQI")
plt.xlabel("Pollutant")
plt.ylabel("Correlation with AQI")
plt.xticks(
    ticks=range(5),
    labels=["PM2.5", "PM10", "NO2", "SO2", "O3"],
    rotation=0
)

plt.tight_layout()
plt.show()