from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Follow, User
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated 
from rest_framework.decorators import permission_classes
from .serializers import UserSerializer, FollowSerializer, FollowViewSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.core.mail import EmailMessage

class Test(APIView):
    def post(self,request):
        EmailMessage(
            # 제목
            "subject",        
            # 이메일 내용
            "content",
            # 보내는 사람
            "luckguy@B18.com",
            # 받는 사람
            ["insert@email.me"],
        ).send()
        return Response(status=status.HTTP_200_OK)

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
#________ btoken __________________
      
class TokenBlacklistView(APIView):
    '''로그아웃 - refresh token blacklist'''
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success")