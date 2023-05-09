from rest_framework import serializers
from .models import User, Follow


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

class FollowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name']
        
class FollowSerializer(serializers.ModelSerializer):
    follow = FollowUserSerializer(read_only=True)
    follower = FollowUserSerializer(read_only=True)
    
    class Meta:
        model = Follow
        fields = "__all__"
                
        
