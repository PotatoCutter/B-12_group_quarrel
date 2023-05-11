from random import randint,choice
import random
import string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Follow, User
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import permission_classes
from .serializers import UserSerializer, FollowSerializer, FollowViewSerializer, UserForgotPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage


class EmailCert(APIView):
    def post(self,request):
        '''이메일 인증'''
        try:
            # 사용자의 req 의 email을 가져와 user의 email 비교 객체를 가져옴
            user = User.objects.get(email=request.data['email'])
            # user객체의 코드와 사용자의 req의 코드를 비교
            if user.create_code == request.data['code']:
                # 해당 사용자의 user를 활성화
                user.is_active = True
                user.save()
                return Response({"message":"이메일 인증"},status=status.HTTP_200_OK)
                
        except:
            return Response({"message":"이메일 인증 실패"},status=status.HTTP_400_BAD_REQUEST)

class RegenerationCert(APIView):
    def post(self,request):
        '''재생성 인증번호 발송'''
        user = User.objects.get(email=request.data['email'])
        user.create_code = str(randint(1,999999)).zfill(6)
        user.save()
        
        # 변경된 인증 메일 전송
        EmailMessage(
            # 제목
            "시비시비 커뮤니티 회원인증",        
            # 이메일 내용
            user.create_code,
            # 보내는 사람
            "luckguy@B18.com",
            # 받는 사람
            [request.data['email']],
        ).send()
        
        return Response(status=status.HTTP_200_OK)
        
class ForgotPassword(APIView):
    def post(self, request):
        '''Forgot password'''
        try:
            # 사용자의 req 의 email을 가져와 user의 email 비교 객체를 가져옴
            user = User.objects.get(email=request.data['email'])
            # user객체의 코드와 사용자의 req의 코드를 비교
            if user.create_code == request.data['code']:
                serial = UserForgotPasswordSerializer().password_reset(user)
                serial.save()
                return Response({"message":"비밀번호 변경 성공"},status=status.HTTP_200_OK)
                
        except:
            return Response({"message":"이메일 인증 실패"},status=status.HTTP_400_BAD_REQUEST)


#______ user CRUD ________
class SignupView(APIView):
    def post(self, request):
        '''유저 생성'''
        user = UserSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        user.save()
        return Response({"message":"signup ok"},status=status.HTTP_201_CREATED)
    
@permission_classes([IsAuthenticatedOrReadOnly])
class UserView(APIView):

    def get(self, request, user_id=None):
        '''유저 조회'''
        user = User.objects.get(id=user_id)
        serial = UserSerializer(user)
        return Response(serial.data)
    
    def put(self, request, user_id=None):
        '''유저 수정'''
        # 나중에 수정 해야함. get_or_404
        if str(request.user) == "AnonymousUser":
            return Response({"message":"익명 유저"}, status=status.HTTP_403_FORBIDDEN)
        # end line
        
        # id 있을때
        if user_id:
            user = get_object_or_404(User, id=user_id)
            if request.user == user:
                serial = UserSerializer(user, request.data)
                if serial.is_valid(raise_exception=True):
                    serial.save()
                    return Response(serial.data, status=status.HTTP_200_OK)
        # id 없을때
        return Response( status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, user_id=None):
        '''유저 삭제'''
        user =  get_object_or_404(User, id =user_id)
        if request.user == user:
            user.delete()
            return Response({"message":"유저 삭제"}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

#________ user end of code __________

#________ follow ____________________
class FollowView(APIView):
    def post(self, request):
        follower = request.user # 현재 로그인한 유저
        follow_data = {'fl': follower.id, 'fw': request.data.get('fw')}
        serializer = FollowSerializer(data=follow_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Follow complete:D"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, user_id):
        follows = Follow.objects.filter(fl_id=user_id)
        serializer = FollowViewSerializer(follows, many=True)
        return Response(serializer.data)
    
    def delete(self, request, user_id):
        follower_id = request.user.id  # 현재 로그인한 사용자의 ID
        try:
            follow = Follow.objects.get(fl_id=follower_id, fw_id=user_id)
            follow.delete()
            return Response({"message": "Unfollowed successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Follow.DoesNotExist:
            pass
        return Response({"message":"Follow does not exist"}, status=status.HTTP_404_NOT_FOUND)

    
class FollowersView(APIView):
    def get(self, request, user_id):
        followers = Follow.objects.filter(fw_id=user_id)
        serializer = FollowViewSerializer(followers, many=True)
        return Response(serializer.data)    
#________ btoken __________________
      
class TokenBlacklistView(APIView):
    '''로그아웃 - refresh token blacklist'''
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success")
    
