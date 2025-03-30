import requests
import psycopg2
import os
from datetime import datetime
import time

API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Klucz API
CITIES = ["Warsaw", "Paris", "Berlin", "London"]
DB_CONFIG = {
    "dbname": "weather_db",
    "user": "postgres",
    "password": "password",
    "host": "db",
    "port": 5432
}


def fetch_weather():
    data = []
    for city in CITIES:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data.append({
                "city": city,
                "temperature": response.json()["main"]["temp"],
                "humidity": response.json()["main"]["humidity"],
                "timestamp": datetime.utcnow()
            })
        else:
            print(f"Błąd pobierania danych dla {city}: {response.json()}")
    return data


def save_to_db(weather_data):
    # Dodajemy logikę ponawiania połączenia
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO weather (city, temperature, humidity, timestamp) VALUES (%s, %s, %s, %s)",
                (weather_data["city"], weather_data["temperature"], weather_data["humidity"], weather_data["timestamp"])
            )
            conn.commit()
            cursor.close()
            conn.close()
            print("Dane zapisane w bazie.")
            break  # Po udanym połączeniu przerywamy pętlę
        except psycopg2.OperationalError as e:
            print(f"Błąd połączenia z bazą danych: {e}")
            retries -= 1
            if retries == 0:
                print("Nie udało się połączyć z bazą danych po kilku próbach. Zatrzymuję aplikację.")
                raise e  # Rzucenie wyjątku, jeśli po kilku próbach nadal nie udało się połączyć
            time.sleep(5)  # Czekamy 5 sekund przed ponowną próbą


if __name__ == "__main__":
    weather_data_list = fetch_weather()
    if weather_data_list:
        for weather_data in weather_data_list:
            save_to_db(weather_data)
    else:
        print("Brak danych pogodowych do zapisania.")