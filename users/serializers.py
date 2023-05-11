from random import randint
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
            "is_active": {
                "write_only": True,
            },
            "is_admin": {
                "write_only": True,
            },
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.age = 0
        password = user.password
        user.set_password(password)
        # 유저에 처음 가입시 코드 생성
        user.create_code = str(randint(1,999999)).zfill(6)
        user.save()
        return user

class FollowViewSerializer(serializers.ModelSerializer):
    follow = serializers.CharField(source='fw.name', read_only=True)
    follower = serializers.CharField(source='fl.name', read_only=True)
    
    class Meta:
        model = Follow
        fields =['follow','follower']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
     #자기자신 팔로우 안되도록 check   
    def check(self, following):
        fw = following.get('fw')
        fl = following.get('fl')
        
        if fw == fl:
            raise serializers.ValidationError("자기 자신은 팔로우할 수 없습니다")
        
        return following
    #check 실행
    def validate(self, data):
        data = super().validate(data)
        return self.check(data)

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
