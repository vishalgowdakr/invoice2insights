# urls.py
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, CustomerViewSet, SupplierViewSet, SaleViewSet,
    SaleDetailViewSet, PurchaseViewSet, PurchaseDetailViewSet,
    ExpenseViewSet, FinancialTransactionViewSet,
    MyTokenObtainPairView, RegisterView, InvoiceView, CurrentUserView,
    BatchUploadAPIView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'sale-details', SaleDetailViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'purchase-details', PurchaseDetailViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'financial-transactions', FinancialTransactionViewSet)
router.register(r'invoices', InvoiceView)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('user/', CurrentUserView.as_view(), name='current_user'),
    path('upload/', BatchUploadAPIView.as_view(), name='batch-upload'),
]
