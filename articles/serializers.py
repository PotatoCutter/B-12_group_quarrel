from rest_framework import serializers
from articles.models import Article, Comment, Bookmark, ArticleLikes, CommentLikes


class ArticleLikeCountSerializer(serializers.ModelSerializer):
    article_likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ArticleLikes
        fields = ['article_likes_count']
        

class BookmarkCountSerializer(serializers.ModelSerializer):
    bookmark_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Bookmark
        fields = ['bookmark_count']


class ArticleSerializer(serializers.ModelSerializer):
    article_likes_count = serializers.SerializerMethodField()
    bookmark_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'

    def get_article_likes_count(self, obj):
        article_likes = ArticleLikes.objects.filter(article=obj).count()
        return article_likes
    
    def get_comment_likes_count(self, obj):
        comment_likes = CommentLikes.objects.filter(comment=obj).count()
        return comment_likes
    
    def get_bookmark_count(self, obj):
        bookmark_count = Bookmark.objects.filter(article=obj).count()
        return bookmark_count


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["title", "content", "article_image"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["comment"]


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'
