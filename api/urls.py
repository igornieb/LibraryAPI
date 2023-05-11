from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from api.views import *

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('books/', BookList.as_view(), name='book-list'),
]
