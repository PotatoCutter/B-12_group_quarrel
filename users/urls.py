from django.urls import path
from users import views

urlpatterns = [
    path('signup/', views.SignupView.as_view()),
    # 세션기반 로그인입니다
    path('login/', views.Login.as_view(), name='login_view'),
    path('<int:user_id>/', views.UserView.as_view()),
]
