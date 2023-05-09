from django.urls import path
from users import views

urlpatterns = [
    path('signup/', views.SignupView.as_view()),
    path('<int:user_id>/', views.UserView.as_view()),
    path('follow/', views.FollowView.as_view()),
    path('followers/<int:user_id>/', views.FollowersView.as_view(), name='followers'),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='following'),
]
