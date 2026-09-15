USE weather_aqi;

-- 7-day rolling average AQI for each city

WITH daily_aqi AS (
    SELECT
        city,
        date,
        avg_aqi
    FROM air_quality
)

SELECT
    city,
    date,
    avg_aqi,
    ROUND(
        AVG(avg_aqi) OVER (
            PARTITION BY city
            ORDER BY date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS rolling_7_day_aqi
FROM daily_aqi
ORDER BY city, date;

-- Identify days where AQI is above 100
-- and examine the rolling AQI

WITH rolling_aqi AS (
    SELECT
        city,
        date,
        avg_aqi,
        ROUND(
            AVG(avg_aqi) OVER (
                PARTITION BY city
                ORDER BY date
                ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
            ),
            2
        ) AS rolling_7_day_aqi
    FROM air_quality
)

SELECT
    city,
    date,
    avg_aqi,
    rolling_7_day_aqi
FROM rolling_aqi
WHERE rolling_7_day_aqi > 100
ORDER BY rolling_7_day_aqi DESC;

-- Worst AQI day for each city

WITH ranked_aqi AS (
    SELECT
        city,
        date,
        avg_aqi,
        max_aqi,
        RANK() OVER (
            PARTITION BY city
            ORDER BY avg_aqi DESC
        ) AS aqi_rank
    FROM air_quality
)

SELECT
    city,
    date,
    avg_aqi,
    max_aqi
FROM ranked_aqi
WHERE aqi_rank = 1
ORDER BY avg_aqi DESC;

-- Compare average AQI between August and September

SELECT
    city,
    MONTH(date) AS month,
    ROUND(AVG(avg_aqi), 2) AS average_aqi,
    ROUND(MAX(avg_aqi), 2) AS highest_aqi,
    ROUND(AVG(avg_pm2_5), 2) AS average_pm2_5,
    COUNT(*) AS days
FROM air_quality
GROUP BY city, MONTH(date)
ORDER BY city, month;

-- August vs September AQI percentage change

WITH monthly_aqi AS (
    SELECT
        city,
        MONTH(date) AS month,
        AVG(avg_aqi) AS average_aqi
    FROM air_quality
    GROUP BY city, MONTH(date)
),

pivoted_aqi AS (
    SELECT
        city,
        MAX(CASE WHEN month = 8 THEN average_aqi END) AS august_aqi,
        MAX(CASE WHEN month = 9 THEN average_aqi END) AS september_aqi
    FROM monthly_aqi
    GROUP BY city
)

SELECT
    city,
    ROUND(august_aqi, 2) AS august_aqi,
    ROUND(september_aqi, 2) AS september_aqi,
    ROUND(
        ((september_aqi - august_aqi) / august_aqi) * 100,
        2
    ) AS percentage_change
FROM pivoted_aqi
ORDER BY percentage_change DESC;

-- City AQI consistency analysis

SELECT
    city,
    ROUND(AVG(avg_aqi), 2) AS average_aqi,
    ROUND(STDDEV(avg_aqi), 2) AS aqi_stddev,
    ROUND(MIN(avg_aqi), 2) AS minimum_aqi,
    ROUND(MAX(avg_aqi), 2) AS maximum_aqi,
    SUM(
        CASE
            WHEN avg_aqi > 100 THEN 1
            ELSE 0
        END
    ) AS days_above_100
FROM air_quality
GROUP BY city
ORDER BY average_aqi DESC;