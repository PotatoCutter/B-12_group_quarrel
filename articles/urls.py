from django.urls import path
from articles import views

urlpatterns = [
    path('<int:category_id>/',views.ArticleListView.as_view(), name = 'article_detail_view'),
    path('detail/<int:article_id>/',views.ArticleDetailView.as_view(), name = 'article_detail_view'),
]