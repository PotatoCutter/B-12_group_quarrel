from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }

    def create(self, validated_data):
        # passwords = request.data.pop('password')
        # user = User(**request.data)
        # user.set_password(passwords)
        # user.save()
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

class BTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["name"] = user.name
        token["email"] = user.email
        token["gender"] = user.gender
        token["age"] = user.age
        token["date_of_birth"] = user.date_of_birth
        
        return token