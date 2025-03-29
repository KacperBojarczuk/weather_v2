CREATE TABLE weather (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50),
    temperature FLOAT,
    humidity INT,
    timestamp TIMESTAMP
);