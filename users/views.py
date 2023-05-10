from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import UserSerializer
# 세션기반 로그인용
from django.contrib.auth import login, get_user_model
from django.contrib import auth


# 회원가입
class SignupView(APIView):
    def post(self, request):
        '''유저 생성'''
        user = UserSerializer(data=request.data)
        # print(user, request.data)
        #
        user.is_valid(raise_exception=True)
        user.save()
        return Response({"message":"signup ok"},status=status.HTTP_201_CREATED)
    

# 로그인
class Login(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = auth.authenticate(request, email=email, password=password)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            login(request, user)
            return Response({"msg": "Login 완료"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "email 또는 password가 틀렸거나 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)


class UserView(APIView):
    def get(self, request):
        '''유저 조회'''
        pass
    def put(self, request):
        '''유저 수정'''
        pass
    def delete(self, request):
        '''유저 삭제'''
        pass
