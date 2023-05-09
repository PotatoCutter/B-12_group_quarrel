from django.db import models
from users.models import User


# 카테고리
class Categorys(models.Model):
    category = models.CharField(max_length=30)


# 게시글
class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, null=False)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.title)
    
    
# 댓글
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=80)
    comm_create_at = models.DateTimeField(auto_now_add=True)
    # 댓글좋아요 cl_id 비식별?
    
    
# 게시글 좋아요
class Likes(models.Model):
    pass


# 댓글 좋아요
class Comment_Likes(models.Model):
    pass


# 북마크 조회
class Bookmark(models.Model):
    pass