import requests

def get_weather_info(ip_address):
    # Example using a weather API (replace with actual API)
    weather_api_url = f"https://api.example.com/weather?ip={ip_address}"
    response = requests.get(weather_api_url)
    if response.status_code == 200:
        data = response.json()
        location = data.get('location', 'Unknown')
        temperature = data.get('temperature', 'Unknown')
    else:
        location = 'Unknown'
        temperature = 'Unknown'
    return location, temperature