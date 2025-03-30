import requests
import psycopg2
import os
from datetime import datetime
import time

API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Klucz API
CITY = "Warsaw"
DB_CONFIG = {
    "dbname": "weather_db",
    "user": "postgres",
    "password": "password",
    "host": "db",
    "port": 5432
}


def fetch_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        return {
            "city": CITY,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "timestamp": datetime.utcnow()
        }
    else:
        print(f"Błąd pobierania danych: {data}")
        return None


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
    weather_data = fetch_weather()
    if weather_data:
        save_to_db(weather_data)

