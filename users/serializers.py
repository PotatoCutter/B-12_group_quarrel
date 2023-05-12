
from random import randint
import random
import string
from rest_framework import serializers
from .models import User, Follow
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import EmailMessage


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
        # user.age = 0
        password = user.password
        user.set_password(password)
        # 유저에 처음 가입시 코드 생성
        user.create_code = str(randint(1,999999)).zfill(6)
        EmailMessage(
            # 제목
            "시비시비 커뮤니티 회원인증",        
            # 이메일 내용
            user.create_code,
            # 보내는 사람
            "luckguy@B18.com",
            # 받는 사람
            [user.email],
        ).send()
        user.save()
        return user
        

class UserForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password',)
        
    def password_reset(self,instance):
        instance.create_code =  str(randint(1,999999)).zfill(6)
        temp_pass = ""
        temp_pass_pool = string.ascii_letters + string.digits + string.punctuation
        for i in range(16):
            temp_pass += random.choice(temp_pass_pool)
        
        instance.password = temp_pass
        print(instance.password, instance.email,instance.create_code)
        EmailMessage(
                    # 제목
                    "시비시비 커뮤니티 새 비밀번호",        
                    # 이메일 내용
                    instance.password,
                    # 보내는 사람
                    "luckguy@B18.com",
                    # 받는 사람
                    [instance.email]
                ).send()
        instance.set_password(temp_pass)
        # instance.save()
        return instance

class FollowViewSerializer(serializers.ModelSerializer):
    follow = serializers.CharField(source='fl.name', read_only=True)
    follower = serializers.CharField(source='fw.name', read_only=True)
    
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
        # token["age"] = user.age
        token["date_of_birth"] = user.date_of_birth
        
        return token
