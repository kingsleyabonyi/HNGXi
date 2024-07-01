from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests, os

from .serializers import HelloSerializer

class HelloView(APIView):
    def get(self, request):
        visitor_name = request.query_params.get('visitor_name', 'Nnamdi')
        client_ip = request.META.get('REMOTE_ADDR')

        
        # IP Geolocation API (for demonstration, we'll use a placeholder)
        # Ideally, use a service like ipinfo.io or ipstack.com to get location from IP
        geolocation_api_url = f"https://ipinfo.io/{client_ip}/json"
        geolocation_response = requests.get(geolocation_api_url)
        geolocation_data = geolocation_response.json()
        location = geolocation_data.get('city', 'Unknown City')

        weather_api_key = os.getenv('a658434e15cf2e723f2f61758f5ba9b8')
        weather_api_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={weather_api_key}"
        weather_response = requests.get(weather_api_url)
        weather_data = weather_response.json()
        temperature = weather_data['main']['temp'] if 'main' in weather_data else 'Unknown'
        
        
        location = "Nsukka"
        temperature = 11

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