from django.urls import path
from .views import UserList, UserFindById

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserFindById.as_view(), name='user-find')
]