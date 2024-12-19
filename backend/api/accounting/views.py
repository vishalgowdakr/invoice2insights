from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from .models import Product, Customer, Supplier, Sale, SaleDetail, Purchase, PurchaseDetail, Expense, FinancialTransaction, Invoice
from accounting.serializers import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import (
    ProductSerializer, CustomerSerializer, SupplierSerializer, SaleSerializer,
    SaleDetailSerializer, PurchaseSerializer, PurchaseDetailSerializer,
    ExpenseSerializer, FinancialTransactionSerializer, UserRegistrationSerializer,
    InvoiceSerializer
)
from .utils.utils import StructuredDataExtractor


class UserOwnedModelViewSet(viewsets.ModelViewSet):
    """
    A base class for ensuring that only the data owned by the logged-in user is accessible.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter the queryset to only include the objects owned by the logged-in user
        return super().get_queryset().filter(created_by=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the logged-in user when creating an object
        serializer.save(created_by=self.request.user)

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


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class SaleViewSet(UserOwnedModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


class SaleDetailViewSet(viewsets.ModelViewSet):
    queryset = SaleDetail.objects.all()
    serializer_class = SaleDetailSerializer


class PurchaseViewSet(UserOwnedModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


class PurchaseDetailViewSet(viewsets.ModelViewSet):
    queryset = PurchaseDetail.objects.all()
    serializer_class = PurchaseDetailSerializer


class ExpenseViewSet(UserOwnedModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class FinancialTransactionViewSet(UserOwnedModelViewSet):
    queryset = FinancialTransaction.objects.all()
    serializer_class = FinancialTransactionSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class InvoiceView(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, serializer):
        serializer.save(user=self.request.user)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'user_id': request.user.id,
            'username': request.user.username,
            'is_authenticated': request.user.is_authenticated
        })


class FileUploadView(APIView):
    parser_classes = [FileUploadParser]
    permission_classes = [IsAuthenticated]

    def put(self, request, filename):
        file_obj = request.data['file']
        invoice = Invoice(invoice_file=file_obj, user=request.user)
        invoice.save()
        # check the file extension
        extension = filename.split('.')[-1]
        if extension not in ['jpg', 'png']:
            return Response(status=400)
        file_path = invoice.invoice_file.path
        print('file_path', invoice.invoice_file.path)
        structured_data_extractor = StructuredDataExtractor(file_path)
        structured_data_extractor.extract()
        return Response(status=204)
