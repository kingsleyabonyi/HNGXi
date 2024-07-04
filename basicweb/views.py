from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests, os
from decouple import config

from .serializers import HelloSerializer

class HelloView(APIView):
    def get(self, request):
        visitor_name = request.query_params.get('visitor_name', 'Nnamdi')
        
        # Extract client IP from request (example, might need adjustment based on your setup)
        client_ip = '197.210.0.0'  # Default IP for testing

        # IP Geolocation API (replace with your actual service)
        geolocation_api_url = f"https://ipinfo.io/{client_ip}/json"
        try:
            geolocation_response = requests.get(geolocation_api_url)
            geolocation_response.raise_for_status()
            geolocation_data = geolocation_response.json()
            location = geolocation_data.get('city', 'Unknown City')
        except requests.RequestException as e:
            location = 'Unknown City'

        # Get weather API key from environment variable
        weather_api_key = config('WEATHER_API_KEY')
        
        if not weather_api_key:
            return Response({"error": "Weather API key not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print(f"Weather API Key: {weather_api_key}")
        # Fetch weather data
        weather_api_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={weather_api_key}"
        try:
            weather_response = requests.get(weather_api_url)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            temperature = weather_data['main']['temp'] if 'main' in weather_data else 'Unknown'
        except requests.RequestException as e:
            temperature = 'Unknown'

        greeting = f"Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {location}"

        data = {
            'client_ip': client_ip,
            'location': location,
            'greeting': greeting
        }

        serializer = HelloSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)