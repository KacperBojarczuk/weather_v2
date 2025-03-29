FROM python:3.10
WORKDIR /app
COPY fetch_weather.py requirements.txt ./
RUN pip install -r requirements.txt
CMD ["python", "fetch_weather.py"]