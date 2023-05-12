from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from articles.models import Categorys, Article, Comment, ArticleLikes, CommentLikes, Bookmark
from articles.serializers import ArticleSerializer, ArticleCreateSerializer, CommentCreateSerializer, CommentSerializer, BookmarkSerializer
from django.db.models import Count


# 카테고리별 메인페이지
class ArticleListView(APIView):
    def get(self, request, category_id):
        articles = Article.objects.filter(category_id=category_id).order_by('-create_at')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, category_id):
        serializer = ArticleCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, category_id=category_id)
            return Response({"message":"게시글 등록완료"}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 게시글 좋아요순
class ArticleBestListView(APIView):
    def get(self, request, category_id):
        articles = Article.objects.filter(category_id=category_id).annotate(like=Count('articlelikes')).order_by('-like')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)


# 게시글 상세페이지
class ArticleDetailView(APIView):
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 게시글 수정하기
    def put(self, request, article_id) :
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user :
            serializer = ArticleCreateSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"수정이 되었습니다."}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"권한이 없습니다."},status=status.HTTP_403_FORBIDDEN)

    # 게시글 삭제하기
    def delete(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            article.delete()
            return Response({"message":"삭제가 되었습니다."},status=status.HTTP_204_NO_CONTENT)
        else :
            return Response({"message":"권한이 없습니다."},status=status.HTTP_403_FORBIDDEN)
        

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
    permission_classes = [permissions.IsAuthenticated]
    
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
    

# 게시글 좋아요 등록, 취소
class ArticleLikesView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        try:
            articlelikes = ArticleLikes.objects.get(article=article, user=request.user)
            articlelikes.delete()
            return Response({"message": "좋아요를 취소했습니다"}, status=status.HTTP_200_OK)
        except ArticleLikes.DoesNotExist:
            articlelikes = ArticleLikes.objects.create(article=article, user=request.user)
            return Response({"message": "좋아요를 눌렀습니다"}, status=status.HTTP_200_OK)


# 댓글 좋아요 등록, 취소 / 505오류....
class CommentLikesView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        try:
            commentlikes = CommentLikes.objects.get(comment=comment, user=request.user)
            commentlikes.delete()
            return Response({"message": "좋아요를 취소했습니다"}, status=status.HTTP_200_OK)
        except CommentLikes.DoesNotExist:
            commentlikes = CommentLikes.objects.create(comment=comment, user=request.user)
            return Response({"message": "좋아요를 눌렀습니다"}, status=status.HTTP_200_OK)


# 북마크 게시글 조회, 등록, 취소
class BookMarkView(APIView):
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        try:
            bookmark = Bookmark.objects.get(article=article, user=request.user)
            bookmark.delete()
            return Response("북마크를 취소했습니다.", status=status.HTTP_200_OK)
        except Bookmark.DoesNotExist:
            bookmark = Bookmark.objects.create(article=article, user=request.user)
            return Response("북마크를 추가하였습니다.", status=status.HTTP_200_OK)

    def get(self, request, user_id):
        bookmark = Bookmark.objects.filter(user_id=user_id)
        serializer = BookmarkSerializer(bookmark, many=True)
        return Response(serializer.data)        


# 내가 쓴 게시글 조회
class ArticleUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, user_id):
        articles = Article.objects.filter(user_id=user_id)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)