from rest_framework import serializers
from .models import User, Service, Auction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'password', 'credit')
        
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'uid', 'name', 'des', 'img', 'option', 'offeruser','maxval', 'date')
        
class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('buyer', 'sid', 'offerprice', 'des')        
        