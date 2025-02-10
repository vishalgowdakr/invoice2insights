from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.contrib.auth.models import User
from django.http import JsonResponse


from accounting.serializers import MyTokenObtainPairSerializer, RegisterSerializer
from accounting.tasks import run_data_extraction_task

from .serializers import (
    UploadSerializer,
)
from .models import Invoice


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


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Upload, Invoice

class BatchUploadAPIView(APIView):
    # If you require authentication you can add permission classes here
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        # Get the file type from the request data.
        print(request.data)
        file_type = request.data.get('file_type')
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
        serializer = UploadSerializer(upload_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TaskAPIView(APIView):
    def post(self, request, upload_id):
        try:
            upload = Upload.objects.get(id=upload_id)
            run_data_extraction_task.delay(upload_id)
        except Upload.DoesNotExist:
            return Response({'error': 'Upload not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'Data extraction task started.'}, status=status.HTTP_200_OK)

    def get(self, request, upload_id):
        try:
            upload = Upload.objects.get(id=upload_id)
            invoices = Invoice.objects.filter(upload_id=upload_id)
            progress = sum(invoice.analyzed for invoice in invoices if invoice.analyzed == True) / len(invoices)
            task_status = 'Completed' if progress == 1 else 'In Progress'
        except:
            return Response({'error': 'Upload not found.'}, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse({
            'upload_id': upload_id,
            'progress': progress,
            'status': task_status
        })
