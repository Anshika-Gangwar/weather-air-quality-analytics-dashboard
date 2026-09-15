CREATE DATABASE weather_aqi;
USE weather_aqi;
CREATE TABLE weather_data (
id INT AUTO_INCREMENT PRIMARY KEY,
city VARCHAR(50),
date DATE,
temperature DECIMAL(5,2),
humidity DECIMAL(5,2),
precipitation DECIMAL(6,2),
wind_speed DECIMAL(6,2)
);

SHOW TABLES;
DESCRIBE weather_data;

USE weather_aqi;

SELECT COUNT(*) AS total_records
FROM weather_data;

SELECT * FROM weather_data LIMIT 10;
SELECT 
  city,
  AVG(temperature) AS average_temperature
FROM weather_data
GROUP BY city
ORDER BY average_temperature DESC;

SELECT
    city,
    AVG(humidity) AS average_humidity
FROM weather_data
GROUP BY city
ORDER BY average_humidity DESC;

SELECT 
    city, SUM(precipitation) AS total_precipitation
FROM
    weather_data
GROUP BY city
ORDER BY total_precipitation DESC;

SELECT
    city,
    ROUND(MIN(temperature), 2) AS min_temperature,
    ROUND(MAX(temperature), 2) AS max_temperature,
    ROUND(STDDEV(temperature), 2) AS temperature_stddev
FROM weather_data
GROUP BY city
ORDER BY temperature_stddev DESC;

SELECT
    city,
    MONTH(date) AS month,
    ROUND(AVG(temperature), 2) AS avg_temperature,
    ROUND(AVG(humidity), 2) AS avg_humidity,
    ROUND(SUM(precipitation), 2) AS total_precipitation
FROM weather_data
GROUP BY city, MONTH(date)
ORDER BY city, month;

-- air quality data table 

CREATE TABLE air_quality (
   id INT AUTO_INCREMENT PRIMARY KEY,
   city VARCHAR(50),
   date DATE,
   avg_aqi DECIMAL(8,2),
   max_aqi DECIMAL(8,2),
   avg_pm2_5 DECIMAL(8,2),
   avg_pm10 DECIMAL(8,2),
   avg_co DECIMAL(10,2),
   avg_no2 DECIMAL(8,2),
   avg_so2 DECIMAL(8,2),
   avg_o3 DECIMAL(8,2)
);

SHOW TABLES;
DESCRIBE air_quality;

USE weather_aqi;

SELECT COUNT(*) AS total_records
FROM air_quality;

SELECT * FROM air_quality LIMIT 10;

SELECT
    city,
    ROUND(AVG(avg_aqi), 2) AS average_aqi
FROM air_quality
GROUP BY city
ORDER BY average_aqi DESC;

SELECT
    city,
    ROUND(AVG(avg_pm2_5), 2) AS avg_pm2_5,
    ROUND(AVG(avg_pm10), 2) AS avg_pm10,
    ROUND(AVG(avg_no2), 2) AS avg_no2,
    ROUND(AVG(avg_so2), 2) AS avg_so2,
    ROUND(AVG(avg_o3), 2) AS avg_o3
FROM air_quality
GROUP BY city
ORDER BY avg_pm2_5 DESC;

SELECT
    city,
    date,
    avg_aqi
FROM air_quality
WHERE (city, avg_aqi) IN (
    SELECT
        city,
        MAX(avg_aqi)
    FROM air_quality
    GROUP BY city
)
ORDER BY avg_aqi DESC;

SELECT
    city,
    ROUND(AVG(avg_aqi), 2) AS average_aqi,
    RANK() OVER (
        ORDER BY AVG(avg_aqi) DESC
    ) AS aqi_rank
FROM air_quality
GROUP BY city
ORDER BY aqi_rank;

-- weather_data + air quality 

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
FROM weather_data w
INNER JOIN air_quality a
    ON w.city = a.city
    AND w.date = a.date
LIMIT 20;

SELECT
    w.city,
    ROUND(AVG(temperature), 2) AS avg_temperature,
    ROUND(AVG(humidity), 2) AS avg_humidity,
    ROUND(AVG(wind_speed), 2) AS avg_wind_speed,
    ROUND(AVG(avg_aqi), 2) AS avg_aqi
FROM weather_data w
INNER JOIN air_quality a
    ON w.city = a.city
    AND w.date = a.date
GROUP BY w.city
ORDER BY avg_aqi DESC;

SELECT
    city,
    date,
    avg_aqi,
    CASE
        WHEN avg_aqi <= 50 THEN 'Good'
        WHEN avg_aqi <= 100 THEN 'Moderate'
        WHEN avg_aqi <= 150 THEN 'Unhealthy for Sensitive Groups'
        WHEN avg_aqi <= 200 THEN 'Unhealthy'
        WHEN avg_aqi <= 300 THEN 'Very Unhealthy'
        ELSE 'Hazardous'
    END AS aqi_category
FROM air_quality
ORDER BY avg_aqi DESC;

SELECT
    city,
    SUM(CASE WHEN avg_aqi <= 50 THEN 1 ELSE 0 END) AS good_days,
    SUM(CASE WHEN avg_aqi BETWEEN 51 AND 100 THEN 1 ELSE 0 END) AS moderate_days,
    SUM(CASE WHEN avg_aqi BETWEEN 101 AND 150 THEN 1 ELSE 0 END) AS unhealthy_sensitive_days,
    SUM(CASE WHEN avg_aqi > 150 THEN 1 ELSE 0 END) AS unhealthy_days
FROM air_quality
GROUP BY city
ORDER BY unhealthy_days DESC;

SELECT
    city,
    date,
    COUNT(*) AS record_count
FROM weather_data
GROUP BY city, date
HAVING COUNT(*) > 1
ORDER BY record_count DESC;

SELECT
    city,
    date,
    COUNT(*) AS record_count
FROM air_quality
GROUP BY city, date
HAVING COUNT(*) > 1
ORDER BY record_count DESC;
