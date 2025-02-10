# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MyTokenObtainPairView, RegisterView,
    BatchUploadAPIView, TaskAPIView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('upload/', BatchUploadAPIView.as_view(), name='batch-upload'),
    path('analyze/<int:upload_id>/', TaskAPIView.as_view(), name='analyze-detail'),  # Integer parameter
]
