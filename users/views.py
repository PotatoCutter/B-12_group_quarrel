from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Follow
from .serializers import UserSerializer, FollowSerializer, FollowViewSerializer
from rest_framework_simplejwt.tokens import RefreshToken



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

class FollowView(APIView):
    def post(self, request):
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Follow complete:D"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, user_id):
        follows = Follow.objects.filter(fl_id=user_id)
        serializer = FollowViewSerializer(follows, many=True)
        return Response(serializer.data)
    
    def delete():
        '''팔로우 삭제'''
        pass
    
class FollowersView(APIView):
    def get(self, request, user_id):
        followers = Follow.objects.filter(fw_id=user_id)
        serializer = FollowViewSerializer(followers, many=True)
        return Response(serializer.data)    

class TokenBlacklistView(APIView):
    '''로그아웃 - refresh token blacklist'''
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success")


