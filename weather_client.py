import requests

class WeatherClient:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    CITIES = {
        "Johannesburg": (-26.2041, 28.0473),
        "Cape Town": (-33.9249, 18.4241),
        "Durban": (-29.8587, 31.0218),
        "Pretoria": (-25.7479, 28.2293),
        "Port Elizabeth": (-33.9608, 25.6022),
    }

    def __init__(self, timeout=10):
        self.timeout = timeout

    def fetch_current(self,city_name):
        if city_name not in self.CITIES:
            return None
        lat, lon = self.CITIES[city_name]
        url = f"{self.BASE_URL}?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code"
        try:
            r = requests.get(url, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException:
            print(f"Error fetching weather data for {city_name}")
            return None
        except ValueError:
            print(f"Error: Response from {url} is not valid JSON")
            return None
        
    def list_cities(self):
        return list(self.CITIES.keys())
