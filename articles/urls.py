from django.urls import path
from articles import views

urlpatterns = [
    path('<int:ctg_id>/',views.ArticleListView.as_view(), name = 'article_detail_view'),
    path('<int:ctg_id>/<int:ctt_id>/',views.ArticleDetailView.as_view(), name = 'article_detail_view'),
]