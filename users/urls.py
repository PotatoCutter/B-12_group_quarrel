from django.urls import path
from users import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('signup/', views.SignupView.as_view()),
    path('', views.UserView.as_view()),
    path('<int:user_id>/', views.UserView.as_view()),
    path('follow/', views.FollowView.as_view(), name='following'),
    path('followers/<int:user_id>/', views.FollowersView.as_view(), name='followers'),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follows'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/blacklist/', views.TokenBlacklistView.as_view(), name='token_blacklist'),
]