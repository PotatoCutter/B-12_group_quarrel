from rest_framework import serializers
from .models import User, Follow
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
        user.age = 0
        password = user.password
        user.set_password(password)
        user.save()
        return user

class FollowUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField()  # name 필드를 직렬화
    class Meta:
        model = User
        fields = ['name']
        
class FollowViewSerializer(serializers.ModelSerializer):
    follow = serializers.CharField(source='fl.name', read_only=True)
    follower = serializers.CharField(source='fw.name', read_only=True)
    
    class Meta:
        model = Follow
        fields =['follow','follower']
        # exclude = ['id']    # name값만 나오게 하기

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

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
