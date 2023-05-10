from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Follow, User
from rest_framework.generics import get_object_or_404
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
    def get(self, request, user_id=None):
        '''유저 조회'''
        return Response({"message":"유저 조회"})
    
    def put(self, request, user_id=None):
        '''유저 수정'''
        # 나중에 수정 해야함. get_or_404
        if str(request.user) == "AnonymousUser":
            return Response({"message":"익명 유저"}, status=status.HTTP_403_FORBIDDEN)
        # end line
        
        # id 있을때
        if user_id:
            user = User.objects.filter(id= user_id)
            serial = UserSerializer(user, data=request.data)
            if serial.is_valid(raise_exception=True):
                serial.save()
                return Response(serial.data, status=status.HTTP_200_OK)
        # id 없으면
        user = UserSerializer(request.user, data = request.data) # 검토가 필요 arg 1 
        user.is_valid(raise_exception=True)
        user.save()
        return Response({"message":"유저 정보 수정"}, status=status.HTTP_200_OK)
    
    def delete(self, request, user_id=None):
        '''유저 삭제'''
        user =  get_object_or_404(User, user_id)
        if request.user.id == user:
            user.delete(id= user_id )
            return Response({"message":"유저 삭제"}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
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