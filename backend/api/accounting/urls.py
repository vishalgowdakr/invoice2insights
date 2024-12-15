# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, CustomerViewSet, SupplierViewSet, SaleViewSet,
    SaleDetailViewSet, PurchaseViewSet, PurchaseDetailViewSet,
    ExpenseViewSet, FinancialTransactionViewSet, UserRegistrationView
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

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
]
