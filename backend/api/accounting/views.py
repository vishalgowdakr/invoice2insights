from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from .models import Invoice, IncomingInvoice, Transaction, Product, InvoiceItem
from .serializers import (
    InvoiceSerializer,
    IncomingInvoiceSerializer,
    TransactionSerializer,
    ProductSerializer,
    InvoiceItemSerializer
)


class UserOwnedModelViewSet(viewsets.ModelViewSet):
    """
    A base class for ensuring that only the data owned by the logged-in user is accessible.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter the queryset to only include the objects owned by the logged-in user
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the logged-in user when creating an object
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # Ensure the object being updated belongs to the logged-in user
        if serializer.instance.user != self.request.user:
            raise PermissionDenied(
                "You do not have permission to modify this resource.")
        serializer.save()

    def perform_destroy(self, instance):
        # Ensure the object being deleted belongs to the logged-in user
        if instance.user != self.request.user:
            raise PermissionDenied(
                "You do not have permission to delete this resource.")
        instance.delete()


class InvoiceViewSet(UserOwnedModelViewSet):
    """
    API view for managing Invoices.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class IncomingInvoiceViewSet(UserOwnedModelViewSet):
    """
    API view for managing Incoming Invoices.
    """
    queryset = IncomingInvoice.objects.all()
    serializer_class = IncomingInvoiceSerializer


class TransactionViewSet(UserOwnedModelViewSet):
    """
    API view for managing Transactions.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class ProductViewSet(UserOwnedModelViewSet):
    """
    API view for managing Products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class InvoiceItemViewSet(viewsets.ModelViewSet):
    """
    API view for managing Invoice Items.
    """

    permission_classes = [IsAuthenticated]
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer

    def get_queryset(self):
        # Ensure only items linked to the logged-in user's invoices are returned
        return super().get_queryset().filter(invoice__user=self.request.user)

    def perform_create(self, serializer):
        # Ensure the associated invoice belongs to the logged-in user
        invoice = serializer.validated_data.get('invoice')
        if invoice.user != self.request.user:
            raise PermissionDenied(
                "You do not have permission to add items to this invoice.")
        serializer.save()

    def perform_update(self, serializer):
        # Ensure the associated invoice belongs to the logged-in user
        invoice = serializer.instance.invoice
        if invoice.user != self.request.user:
            raise PermissionDenied(
                "You do not have permission to modify this invoice item.")
        serializer.save()

    def perform_destroy(self, instance):
        # Ensure the associated invoice belongs to the logged-in user
        if instance.invoice.user != self.request.user:
            raise PermissionDenied(
                "You do not have permission to delete this invoice item.")
        instance.delete()


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
