from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Movies, WatchList, WatchedList


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        user = super(RegisterSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=250)
    password = serializers.CharField(max_length=250)


class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = "__all__"

class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = "__all__"

class WatchedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchedList
        fields = "__all__"