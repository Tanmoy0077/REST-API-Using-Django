from django.urls import path
from .views import UserDetail, UserList, LoginView, LogoutView, FacilityDetailsDetail, FacilityDetailsListCreate, \
    WasteTypeListCreate, WasteTypeDetail, \
    RequestStatusListCreateAPIView, FormDetailsListCreateAPIView, FormDetailsAPIView, \
    DisposalDetailsListCreateAPIView, RequestStatusDetailAPIView, DisposalDetailsAPIView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('users/', UserList.as_view()),
    path('users/<str:pk>/', UserDetail.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('facilities/', FacilityDetailsListCreate.as_view(), name='facility-list-create'),
    path('facilities/<int:bldg_no>/', FacilityDetailsDetail.as_view(), name='facility-detail'),

    path('waste-types/', WasteTypeListCreate.as_view(), name='waste-type-list-create'),
    path('waste-types/<str:sl_no>/', WasteTypeDetail.as_view(), name='waste-type-detail'),

    path('request_status/', RequestStatusListCreateAPIView.as_view(), name='request_status_list_create'),
    path('request_status/<int:pk>/', RequestStatusDetailAPIView.as_view(), name='request_status_detail'),

    path('form_details/', FormDetailsListCreateAPIView.as_view(), name='form_details_list_create'),
    path('form_details/<str:pk>/', FormDetailsAPIView.as_view(), name='form_details_detail'),

    path('disposal_details/', DisposalDetailsListCreateAPIView.as_view(), name='disposal_details_list_create'),
    path('disposal_details/<str:pk>/', DisposalDetailsAPIView.as_view(), name='disposal_details_detail'),
]
