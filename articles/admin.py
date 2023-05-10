from django.contrib import admin
from articles.models import Categorys, Article, Comment, ArticleLikes, CommentLikes


admin.site.register(Categorys)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(ArticleLikes)
admin.site.register(CommentLikes)
