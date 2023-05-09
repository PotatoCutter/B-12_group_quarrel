from django.urls import path
from users import views

urlpatterns = [
    path('signup/', views.SignupView.as_view()),
    path('<int:user_id>/', views.UserView.as_view()),
]
