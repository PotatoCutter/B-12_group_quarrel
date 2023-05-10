from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from articles.models import Categorys, Article
from articles.serializers import ArticleSerializer


# 카테고리별 메인페이지
class ArticleListView(APIView):
    def get(self, request, category_id):
        articles = Article.objects.filter(category_id=category_id)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request, category_id):
        serializer = ArticleSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, category_id=category_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 게시글 상세페이지
class ArticleDetailView(APIView):
    def get(self, article_id):
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    # 게시글 수정하기
    def put(self, request, ctt_id) :
        ctt = get_object_or_404(Article, id=ctt_id)
        if request.user == ctt.user :
            serializer = ArticleSerializer(ctt, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"권한이 없습니다."},status=status.HTTP_403_FORBIDDEN)

    # 게시글 삭제하기
    def delete(self, request, ctt_id) :
        ctt = get_object_or_404(Article, id=ctt_id)
        if request.user == ctt.user :
            ctt.delete()
            return Response({"message":"삭제가 되었습니다."},status=status.HTTP_204_NO_CONTENT)
        else :
            return Response({"message":"권한이 없습니다."},status=status.HTTP_403_FORBIDDEN)
        

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
    

# 좋아요 등록, 취소
class Like(APIView):
    def post(self, ctg_id, ctt_id):
        pass


# 북마크 게시글 조회, 등록, 취소
class BookMarkView(APIView):
    def get(self, ctg_id, ctt_id):
        pass
    
    def post(self, ctg_id, ctt_id):
        pass


# 내가 쓴 게시글 조회
class ArticleUserView(APIView):
    def get(self, user_id):
        pass