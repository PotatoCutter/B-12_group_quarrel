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
        user = super().create(validated_data)
        user.age = 0
        password = user.password
        user.set_password(password)
        user.save()
        return user

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.date_of_birth = validated_data.get(
    #         "date_of_birth", instance.date_of_birth)
    #     instance.age = validated_data.get("age", instance.age)
    #     instance.gender = validated_data.get("gender", instance.gender)
    #     instance.profile_photo = validated_data.get(
    #         "profile_photo", instance.profile_photo)
    #     instance.subscript = validated_data.get(
    #         "subscript", instance.subscript)
    #     password = validated_data.get("password", instance.password)
    #     instance.set_password(password)
    #     instance.save()
    #     return instance
