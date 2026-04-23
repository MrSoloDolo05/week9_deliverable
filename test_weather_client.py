import weather_client, pytest, requests

def test_list_cities():
    client = weather_client.WeatherClient()
    cities = client.list_cities()
    assert isinstance(cities, list)
    assert "Johannesburg" in cities
    assert "Cape Town" in cities
    assert "Durban" in cities
    assert "Pretoria" in cities
    assert "Port Elizabeth" in cities

def test_fetch_current_valid_city():
    client = weather_client.WeatherClient()
    weather_data = client.fetch_current("Johannesburg")
    assert weather_data is not None
    assert "current" in weather_data
    assert "temperature_2m" in weather_data["current"]
    assert "weather_code" in weather_data["current"]

def test_fetch_current_invalid_city():
    client = weather_client.WeatherClient()
    weather_data = client.fetch_current("InvalidCity")
    assert weather_data is None

def test_fetch_current_timeout(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.Timeout()
    
    monkeypatch.setattr(requests, "get", mock_get)
    client = weather_client.WeatherClient(timeout=1)
    weather_data = client.fetch_current("Johannesburg")
    assert weather_data is None

def test_fetch_current_invalid_json(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass
        def json(self):
            raise ValueError("Invalid JSON")
    
    def mock_get(*args, **kwargs):
        return MockResponse()
    
    monkeypatch.setattr(requests, "get", mock_get)
    client = weather_client.WeatherClient()
    weather_data = client.fetch_current("Johannesburg")
    assert weather_data is None

def test_fetch_current_http_error(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            raise requests.exceptions.HTTPError("HTTP error")

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    client = weather_client.WeatherClient()
    weather_data = client.fetch_current("Johannesburg")
    assert weather_data is None

def test_fetch_current_request_exception(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.RequestException("Request error")
    
    monkeypatch.setattr(requests, "get", mock_get)
    client = weather_client.WeatherClient()
    weather_data = client.fetch_current("Johannesburg")
    assert weather_data is None

def test_fetch_current_valid_city_with_timeout(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass
        def json(self):
            return {"current": {"temperature_2m": 25, "weather_code": 0}}
    
    def mock_get(*args, **kwargs):
        return MockResponse()
    
    monkeypatch.setattr(requests, "get", mock_get)
    client = weather_client.WeatherClient(timeout=1)
    weather_data = client.fetch_current("Johannesburg")
    assert weather_data is not None
    assert "current" in weather_data
    assert "temperature_2m" in weather_data["current"]
    assert "weather_code" in weather_data["current"]

def test_fetch_current_valid_city_with_invalid_json(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass
        def json(self):
            raise ValueError("Invalid JSON")
    
    def mock_get(*args, **kwargs):
        return MockResponse()
    
    monkeypatch.setattr(requests, "get", mock_get)
    client = weather_client.WeatherClient(timeout=1)
    weather_data = client.fetch_current("Johannesburg")
    assert weather_data is None
 
def test_fetch_current_valid_city_with_http_error(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            raise requests.exceptions.HTTPError("HTTP error")

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    client = weather_client.WeatherClient(timeout=1)
    weather_data = client.fetch_current("Johannesburg")
    assert weather_data is None

