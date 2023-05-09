from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from articles.models import Article
from articles.serializers import ArticleSerializer

# 게시글 상세페이지
class ArticleDetailView(APIView):
    def get(self, ctt_id):
        article = get_object_or_404(Article, id=ctt_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 게시글 수정하기
    def put() :
        pass

    # 게시글 삭제하기    
    def delete() :
        pass

