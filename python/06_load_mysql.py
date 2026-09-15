import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Load environment variables
load_dotenv()

# Read database credentials
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
port = os.getenv("MYSQL_PORT")
database = os.getenv("MYSQL_DATABASE")

# Load CSV
df = pd.read_csv("data/raw/historical_weather.csv")

print("Rows loaded from CSV:", len(df))

# Create MySQL connection
encoded_password = quote_plus(password)
engine = create_engine(
    f"mysql+pymysql://{user}:{encoded_password}@{host}:{port}/{database}"
)

# Load data into MySQL
df.to_sql(
    "weather_data",
    con=engine,
    if_exists="append",
    index=False
)

print("Data successfully loaded into MySQL!")