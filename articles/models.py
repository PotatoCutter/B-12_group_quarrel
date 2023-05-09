from django.db import models
from users.models import User


# 카테고리
class Categorys(models.Model):
    category = models.CharField(max_length=30, verbose_name="카테고리명")
    
    def __str__(self):
        return str(self.category)


# 게시글
class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    Category = models.OneToManyField(Categorys, on_delete=models.CASCADE, verbose_name="카테고리")
    title = models.CharField(max_length=30, null=False, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    def __str__(self):
        return str(self.title)
    
    
# 댓글
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    comment = models.CharField(max_length=80, verbose_name="댓글")
    comm_create_at = models.DateTimeField(auto_now_add=True, verbose_name="댓글 작성일시")
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