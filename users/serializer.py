from rest_framework import serializers
from .models import User


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
