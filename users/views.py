from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializer import UserSerializer

class SignupView(APIView):
    def post(self, request):
        '''유저 생성'''
        user = UserSerializer(data=request.data)
        # print(user, request.data)
        #
        user.is_valid(raise_exception=True)
        user.save()
        return Response({"message":"signup ok"},status=status.HTTP_201_CREATED)
    
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
