from .views import UserRegistrationView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    InvoiceViewSet,
    IncomingInvoiceViewSet,
    TransactionViewSet,
    ProductViewSet,
    InvoiceItemViewSet
)

router = DefaultRouter()
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'incoming-invoices', IncomingInvoiceViewSet,
                basename='incoming-invoice')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'invoice-items', InvoiceItemViewSet, basename='invoice-item')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]
