from django.contrib import admin
from articles.models import Categorys, Article, Comment


admin.site.register(Categorys)
admin.site.register(Article)
admin.site.register(Comment)