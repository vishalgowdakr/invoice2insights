import traceback
import logging
import random
from PIL import Image
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from .models import Product, Customer, Supplier, Sale, SaleDetail, Purchase, PurchaseDetail, Expense, FinancialTransaction, Invoice
from .utils.utils import Purchase as PurchasePydantic
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


logger = logging.getLogger(__name__)


class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get_object_or_first(self, model, **kwargs):
        """
        Helper method to get requested object or fall back to first available
        """
        try:
            return model.objects.get(**kwargs)
        except model.DoesNotExist:
            first_obj = model.objects.first()
            if first_obj:
                logger.warning(
                    f"Requested {model.__name__} with {kwargs} not found. Using first available: {first_obj}")
                return first_obj
            logger.error(f"No {model.__name__} objects available in database")
            raise ValueError(f"No {model.__name__} objects available")

    def generate_purchases(self, users, suppliers, products, data=PurchasePydantic):
        """Generate purchases from parsed data"""
        logger.info(
            f"Starting purchase generation for supplier: {data.supplier_name}")
        try:
            from .models import Purchase, PurchaseDetail
            num = len(data.purchase_details)
            payment_modes = ['Cash', 'Card', 'UPI', 'NetBanking']

            logger.debug(f"Looking up supplier: {data.supplier_name}")
            supplier = self.get_object_or_first(
                Supplier, name=data.supplier_name)

            total_cost = 0
            logger.info("Creating main purchase record")
            created_by = users.first() if users.exists() else None
            if not created_by:
                logger.warning("No users available in database")

            purchase = Purchase.objects.create(
                supplier=supplier,
                total_cost=data.total_cost,
                payment_mode=random.choice(payment_modes),
                created_by=created_by
            )
            logger.debug(f"Created purchase record with ID: {purchase.id}")

            # Create Purchase Details
            logger.info(f"Processing {num} purchase details")
            for i in range(num):
                product_name = data.purchase_details[i].product_name
                logger.debug(f"Processing product: {product_name}")

                product = self.get_object_or_first(Product, name=product_name)
                quantity = data.purchase_details[i].quantity
                cost_price = data.purchase_details[i].cost_price
                subtotal = data.purchase_details[i].subtotal
                total_cost += subtotal

                logger.debug(f"Creating purchase detail - Product: {product_name}, "
                             f"Quantity: {quantity}, Cost: {cost_price}, Subtotal: {subtotal}")

                PurchaseDetail.objects.create(
                    purchase=purchase,
                    product=product,
                    quantity=quantity,
                    cost_price=cost_price,
                    subtotal=subtotal
                )

                # Update product stock
                logger.debug(f"Updating stock for product {product_name} - "
                             f"Adding {quantity} units")
                product.stock_quantity += quantity
                product.save()

            logger.info(f"Purchase generation completed successfully. "
                        f"Total cost: {total_cost}")

        except Exception as e:
            logger.error(f"Error in generate_purchases: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    def put(self, request, filename):
        logger.info(f"Processing file upload request for filename: {filename}")
        logger.debug(f"Request user: {request.user.username}")

        try:
            # Debug request metadata
            logger.debug(f"Content-Type: {request.META.get('CONTENT_TYPE')}")
            logger.debug(f"Request FILES: {request.FILES}")

            # Validate file presence
            if 'file' not in request.FILES:
                logger.warning("No file submitted in request")
                return Response(
                    {"error": "No file was submitted"},
                    status=400
                )

            file_obj = request.FILES['file']
            logger.debug(
                f"Received file: {file_obj.name}, Size: {file_obj.size} bytes")

            # Validate file extension
            allowed_extensions = ['.png', '.jpg', '.jpeg']
            if not any(filename.lower().endswith(ext) for ext in allowed_extensions):
                logger.warning(f"Invalid file format attempted: {filename}")
                return Response(
                    {"error": f"Invalid file format. Allowed formats: {', '.join(allowed_extensions)}"},
                    status=400
                )

            # Create and save invoice
            logger.info("Creating invoice record")
            invoice = Invoice(invoice_file=file_obj, user=request.user)
            invoice.save()
            logger.debug(f"Invoice created with ID: {invoice.id}")

            # Process the file
            file_path = invoice.invoice_file.path
            logger.info(f"Starting data extraction from file: {file_path}")

            structured_data_extractor = StructuredDataExtractor(file_path)
            try:
                logger.debug("Extracting data from file")
                data: PurchasePydantic = structured_data_extractor.extract()

                logger.debug("Fetching required database objects")
                users = User.objects.all()
                suppliers = Supplier.objects.all()
                products = Product.objects.all()

                if not users.exists() or not suppliers.exists() or not products.exists():
                    logger.error(
                        "Required model objects not available in database")
                    return Response(
                        {"error": "Required database objects not available"},
                        status=500
                    )

                logger.info("Generating purchases from extracted data")
                self.generate_purchases(users, suppliers, products, data)

                logger.info("File processing completed successfully")
                return Response(
                    {"json": data.json()},
                    status=200
                )

            except Exception as e:
                logger.error(f"Error processing image: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                return Response(
                    {"error": "Error processing image"},
                    status=500
                )

        except Exception as e:
            logger.error(f"Unexpected error in file upload: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return Response(
                {"error": "Internal server error"},
                status=500
            )
