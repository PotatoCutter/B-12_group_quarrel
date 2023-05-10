from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated 
from rest_framework.decorators import permission_classes
from .serializers import UserSerializer
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

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
        print(user)
        return Response(serial.data)
    
    def put(self, request, user_id=None):
        '''유저 수정'''
        # 나중에 수정 해야함. get_or_404
        if str(request.user) == "AnonymousUser":
            return Response({"message":"익명 유저"}, status=status.HTTP_403_FORBIDDEN)
        # end line
        
        # id 있을때
        if user_id:
            user = User.objects.get(id= user_id)
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


class TokenBlacklistView(APIView):
    '''로그아웃 - refresh token blacklist'''
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success")
