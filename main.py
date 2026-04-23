import weather_client

def main():
    client = weather_client.WeatherClient()
    cities = client.list_cities()
    print("Available cities:")
    for city in cities:
        print(f"- {city}")
    
    city_name = input("Enter a city name to get current weather: ")
    weather_data = client.fetch_current(city_name)
    
    if weather_data:
        print(f"Current weather in {city_name}:")
        print(weather_data)
    else:
        print(f"Could not fetch weather data for {city_name}")

if __name__ == "__main__":  
    main()
    