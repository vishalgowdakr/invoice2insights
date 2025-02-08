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


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounting.models import Invoice

from django.forms import ModelForm
class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_file']

# views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Upload, Invoice

class BatchUploadAPIView(APIView):
    # If you require authentication you can add permission classes here
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # Get the file type from the request data.
        print(request.data)
        file_type = request.data.get('file_type')
        print("*"*100)
        print(file_type)
        valid_types = dict(Upload.FILE_TYPE_CHOICES).keys()
        if file_type not in valid_types:
            return Response(
                {'error': f"Invalid file type. Must be one of: {', '.join(valid_types)}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Retrieve all files under the key "invoice_files"
        files = request.FILES.getlist('invoice_files')
        if not files:
            return Response(
                {'error': "No files provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create a new Upload instance to represent this batch.
        upload_instance = Upload.objects.create(file_type=file_type, user=request.user)

        # Create an Invoice for each file.
        invoices = []
        for file_obj in files:
            invoice = Invoice.objects.create(
                upload=upload_instance,
                invoice_file=file_obj,
            )
            invoices.append(invoice)

        # Serialize the created Invoice instances.
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
