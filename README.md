# Weather Monitoring System

Weather Monitoring System to aplikacja zbierająca dane pogodowe z zewnętrznego API, zapisująca je w bazie PostgreSQL oraz wizualizująca dane za pomocą Grafany.

Projekt miał na celu zastosowanie wiedzy dotyczącej Dockera, Grafany, Prometheusa, Pythona, API oraz PostgreSQL z analizą danych.

DevOps: [Kacper Bojarczuk](https://github.com/KacperBojarczuk)

PostgreSQL, Python, SQL: [Karol Kruszyński](https://github.com/karolkruszynski)

## 🛠 Wymagania

Aby uruchomić projekt, potrzebujesz:

- **Docker** i **Docker Compose**

## 🚀 Instalacja i uruchomienie

1. **Sklonuj repozytorium**

   ```sh
   git clone https://github.com/KacperBojarczuk/weather_v2.git
   cd weather_v2
   ```

2. **Skonfiguruj zmienne środowiskowe**

   - Utwórz plik `.env` w katalogu głównym i dodaj:
     ```ini
     OPENWEATHER_API_KEY=twoj_klucz_api
     ```
   - Upewnij się, że masz aktywny klucz API z [OpenWeather](https://openweathermap.org/).

3. **Uruchom aplikację za pomocą Dockera**

   ```sh
   docker-compose up -d --build
   ```

   Ten proces:

   - Uruchomi bazę danych PostgreSQL,
   - Wystartuje usługę zbierania danych pogodowych,
   - Skonfiguruje Prometheusa do monitorowania aplikacji,
   - Włączy Grafanę do wizualizacji danych.

4. **Sprawdź działające usługi**

   - **PostgreSQL**: `localhost:5432` (dane dostępu w `docker-compose.yml`)
   - **Prometheus**: [http://localhost:9090](http://localhost:9090)
   - **Grafana**: [http://localhost:3000](http://localhost:3000)

5. **Zaloguj się do Grafany**

   - Domyślne dane logowania: `admin` / `admin`
   - Po zalogowaniu dodaj **PostgreSQL** jako źródło danych:
     - Host: `db:5432`
     - Database: `weather_db`
     - User: `postgres`
     - Password: `password`
     - SSL Mode: `disable`
   - Następnie utwórz dashboard i dodaj wykres z zapytaniem:
     ```sql
     SELECT timestamp AS "time", city, temperature FROM weather WHERE timestamp >= now() - interval '1 day' ORDER BY timestamp;
     ```

## 🛑 Zatrzymanie aplikacji

Aby zatrzymać i usunąć kontenery, użyj:

```sh
docker-compose down
```

## 📌 Debugowanie

- Sprawdź logi kontenerów:
  ```sh
  docker-compose logs -f weather_fetcher
  ```
- Sprawdź status bazy danych:
  ```sh
  docker ps
  ```
- Jeśli PostgreSQL nie działa, uruchom go ponownie:
  ```sh
  docker-compose restart db
  ```

## 📜 Licencja

Projekt jest dostępny na licencji MIT.

---

Jeśli masz jakiekolwiek problemy, otwórz **Issue** w repozytorium lub skontaktuj się z autorem!

