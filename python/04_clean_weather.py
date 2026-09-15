import pandas as pd 

df = pd.read_csv("C:/Weather_AQI_Project/data/raw/weather_data.csv")

print(df.head())
print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nData types:")
df["date"] = pd.to_datetime(df["date"])
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())