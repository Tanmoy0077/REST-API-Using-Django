from django.urls import path
from .views import UserDetail, UserList, LoginView


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('users/', UserList.as_view()),
    path('users/<str:pk>/', UserDetail.as_view())
]
