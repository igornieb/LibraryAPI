from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from api.views import *

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/register/', RegisterLibraryUser.as_view(), name='register-user'),
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<str:isbn>/', BookDetails.as_view(), name='book-details')
]
