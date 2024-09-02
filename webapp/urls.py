from django.urls import path
from .views import UserDetail, UserList, LoginView, LogoutView


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('users/', UserList.as_view()),
    path('users/<str:pk>/', UserDetail.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
]
