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
    category = models.ForeignKey(Categorys, on_delete=models.CASCADE, verbose_name="카테고리")
    title = models.CharField(max_length=30, null=False, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    article_image = models.ImageField(blank=True, upload_to='%Y/%m/%d/')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    def __str__(self):
        return str(self.title)


# 댓글
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="해당 게시글")
    comm_content = models.CharField(max_length=80, verbose_name="댓글")
    comm_create_at = models.DateTimeField(auto_now_add=True, verbose_name="댓글 작성일시")
    
    def __str__(self):
        return str(self.comment)


# 게시글 좋아요
class ArticleLikes(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="해당 게시글")
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# 댓글 좋아요
class CommentLikes(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name="해당 댓글")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    
# 북마크 조회
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="제목")