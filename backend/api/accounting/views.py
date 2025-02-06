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
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounting.models import Invoice
from accounting.utils.utils import StructuredDataExtractor

from django.forms import ModelForm
class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_file']

class FileUploadView(APIView):
    parser_classes = [MultiPartParser] # Use MultiPartParser
    permission_classes = [IsAuthenticated]

    def put(self, request, filename):
        # Initialize InvoiceForm with request data
        form = InvoiceForm(request.data, request.FILES) # Important: Pass both request.data and request.FILES

        if form.is_valid(): # Validate the form
            invoice = form.save(commit=False) # Create Invoice instance but don't save to DB yet
            invoice.user = request.user # Set the user from the request
            invoice.save() # Now save to database

            # Check the file extension (good practice - get from saved file)
            file_path = invoice.invoice_file.path
            extension = filename.split('.')[-1].lower() # Get extension from filename URL
            saved_extension = file_path.split('.')[-1].lower() # Get extension from saved file path

            if saved_extension not in ['jpg', 'png', 'jpeg']: # Added jpeg for completeness
                return Response({"error": "Invalid file extension. Allowed extensions are jpg, png, jpeg."}, status=400)

            print('file_path', file_path) # Debug: Verify file path

            structured_data_extractor = StructuredDataExtractor(file_path)
            structured_data = structured_data_extractor.extract() # Process the image

            if structured_data:
                print("Structured data extracted successfully.")
                # You can process or return the structured_data here if needed
            else:
                print("Error during structured data extraction.")
                # Handle extraction error if needed

            return Response(status=204) # 204 No Content - Upload successful
        else:
            # Form is invalid, return errors
            print("Form is invalid:", form.errors) # Debug form errors
            return Response(form.errors, status=400) # Return form errors in response
