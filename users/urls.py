from django.urls import path
from users import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('signup/', views.SignupView.as_view()),
    path('', views.UserView.as_view()),
    path('<int:user_id>/', views.UserView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/blacklist/', views.TokenBlacklistView.as_view(), name='token_blacklist'),
]
