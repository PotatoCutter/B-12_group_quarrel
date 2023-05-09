from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from articles.models import Article
from articles.serializers import ArticleSerializer


# 카테고리별 메인페이지
class ArticleListView(APIView):
    def get(self, ctg_id):
        pass
    
    def post(self, ctg_id, ctt_id):
        pass


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


# 댓글 조회, 등록, 수정, 삭제
class CommentView(APIView):
    def get(self, ctg_id, ctt_id, cm_id):
        pass
    
    def post(self, ctg_id, ctt_id, cm_id):
        pass
    
    def put(self, ctg_id, ctt_id, cm_id):
        pass
    
    def delete(self, ctg_id, ctt_id, cm_id):
        pass
    

# 좋아요 등록/삭제
class Like(APIView):
    def post(self, ctg_id, ctt_id):
        pass


# 북마크 게시글 조회, 등록, 삭제
class BookMarkView(APIView):
    def get(self, ctg_id, ctt_id):
        pass
    
    def post(self, ctg_id, ctt_id):
        pass


# 내가 쓴 게시글 조회
class ArticleUserView(APIView):
    def get(self, user_id):
        pass