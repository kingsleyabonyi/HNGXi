from rest_framework import serializers

class HelloSerializer(serializers.Serializer):
    client_ip = serializers.CharField(max_length=15)
    location = serializers.CharField(max_length=100)
    greeting = serializers.CharField(max_length=255)