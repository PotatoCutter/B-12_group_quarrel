from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from articles.models import Categorys, Article, Comment
from articles.serializers import ArticleSerializer, ArticleCreateSerializer, CommentSerializer, CommentCreateSerializer


# 카테고리별 메인페이지
class ArticleListView(APIView):
    def get(self, request, category_id):
        articles = Article.objects.filter(category_id=category_id)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request, category_id):
        # 로그인 한 유저가 아닐 시 권한없음 else문 필요!
        serializer = ArticleCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, category_id=category_id)
            return Response({"message":"게시글 등록완료"}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 게시글 상세페이지
class ArticleDetailView(APIView):
    def get(self, request, article_id):
        article = Article.objects.get(id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 게시글 수정하기
    def put() :
        pass

    # 게시글 삭제하기
    def delete() :
        pass


# 댓글 조회, 등록
class CommentView(APIView):
    
    # 댓글 전체조회
    def get(self, request, article_id):
        article = Article.objects.get(id=article_id)
        comments = article.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 댓글 등록
    def post(self, request, article_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id)
            return Response({"message":"댓글 등록완료"}, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# 댓글 수정, 삭제
class CommentDetailView(APIView):
    
    # 댓글 수정
    def put(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({"message":"댓글 수정완료"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"권한이 없습니다."},status=status.HTTP_400_BAD_REQUEST)
    
    # 댓글 삭제
    def delete(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response({"message":"댓글 삭제완료"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"권한이 없습니다"},status=status.HTTP_400_BAD_REQUEST)
    

# 좋아요 등록, 취소
class Like(APIView):
    def post(self, category_id, article_id):
        pass


# 북마크 게시글 조회, 등록, 취소
class BookMarkView(APIView):
    def get(self, category_id, article_id):
        pass
    
    def post(self, category_id, article_id):
        pass


# 내가 쓴 게시글 조회
class ArticleUserView(APIView):
    def get(self, user_id):
        pass