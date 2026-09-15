import pandas as pd
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
print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nStatistical Summary:")
print(df.describe())

print("\nAverage metrics by city:")

city_summary = df.groupby("city").agg({
    "temperature": "mean",
    "humidity": "mean",
    "wind_speed": "mean",
    "avg_aqi": "mean",
    "avg_pm2_5": "mean",
    "avg_pm10": "mean"
}).round(2)

print(city_summary)

print("\nCorrelation between Temperature and AQI:")

temperature_aqi_corr = df["temperature"].corr(df["avg_aqi"])

print(round(temperature_aqi_corr, 3))

print("\nCorrelation of pollutants with AQI:")

pollutant_columns = [
    "avg_pm2_5",
    "avg_pm10",
    "avg_no2",
    "avg_so2",
    "avg_o3"
]

pollutant_correlations = (
    df[pollutant_columns + ["avg_aqi"]]
    .corr()["avg_aqi"]
    .drop("avg_aqi")
    .sort_values(ascending=False)
)

print(pollutant_correlations.round(3))