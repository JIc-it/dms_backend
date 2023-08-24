from .models import Document, DocumentCategory, DocumentVersion
from .serializers import DocumentSerializer, DocumentCategorySerializer, DocumentVersionSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from local_apps.account.serializers import UserSerializer
from local_apps.account.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import DocumentFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.views import APIView
import json


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class DocumentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Document.objects.filter(document_user=self.request.user).order_by('-created_at')
    serializer_class = DocumentSerializer
    # filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_backends = [SearchFilter]
    # filterset_class = DocumentFilter
    search_fields = ['document_id',
                     'document_name',
                     'document_category__document_category_name'
                     'shared_with__email',
                     'shared_with__first_name',
                     'shared_with__last_name',
                     'document__email',
                     'document__first_name',
                     'document__last_name',
                     ]
    pagination_class = CustomPagination

    def get_queryset(self):
        # queryset = super().get_queryset()
        queryset = Document.objects.filter(document_user=self.request.user,is_delete=False).order_by('-created_at')
        companies = self.request.query_params.getlist('companies')
        department = self.request.query_params.getlist('department')
        shared_with = self.request.query_params.getlist('shared_with')
        reporting_manager = self.request.query_params.getlist('reporting_manager')
        document_category = self.request.query_params.getlist('document_category')
        if companies:
            queryset = queryset.filter(document_user__company__id__in=companies)
        if department:
            queryset = queryset.filter(document_user__department__id__in=department)
        if shared_with:
            queryset = queryset.filter(document_user__shared_with__id__in=shared_with)
        if reporting_manager:
            queryset = queryset.filter(document_user__reporting_manager__id__in=reporting_manager)
        if document_category:
            queryset = queryset.filter(document_category__id__in=document_category)
        return queryset


class SharedDocumentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DocumentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['document_id',
                     'document_name',
                     'document_category__document_category_name'
                     'shared_with__email',
                     'shared_with__first_name',
                     'shared_with__last_name',
                     'document__email',
                     'document__first_name',
                     'document__last_name',
                     ]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Document.objects.filter(shared_with=self.request.user,is_delete=False).order_by('-created_at')
        companies = self.request.query_params.getlist('companies')
        department = self.request.query_params.getlist('department')
        shared_with = self.request.query_params.getlist('shared_with')
        reporting_manager = self.request.query_params.getlist('reporting_manager')
        document_category = self.request.query_params.getlist('document_category')
        if companies:
            queryset = queryset.filter(document_user__company__id__in=companies)
        if department:
            queryset = queryset.filter(document_user__department__id__in=department)
        if shared_with:
            queryset = queryset.filter(document_user__shared_with__id__in=shared_with)
        if reporting_manager:
            queryset = queryset.filter(document_user__reporting_manager__id__in=reporting_manager)
        if document_category:
            queryset = queryset.filter(document_category__id__in=document_category)
        return queryset
        # return Document.objects.filter(shared_with=self.request.user).order_by('-created_at')


class ReportingManagerListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(~Q(reporting_manager=None)).distinct()


class DocumentCategoryListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DocumentCategory.objects.all()
    serializer_class = DocumentCategorySerializer


class DocumentCreateView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def create(self, request, *args, **kwargs):
        try:
            document_category = request.data.get('document_category', None)
            document_category = DocumentCategory.objects.get(id=document_category) if DocumentCategory.objects.filter(
                id=document_category).exists() else None
            shared_with = request.data.get('shared_with', None)
            try:
                shared_with = json.loads(shared_with)
            except json.JSONDecodeError:
                shared_with = None
            shared_with = User.objects.filter(id__in=shared_with) if shared_with else None

            document = Document.objects.create(document_user=request.user,
                                               document_name=request.data.get('document_name', None),
                                               document_category=document_category,
                                               specify_category=request.data.get('specify_category', None),
                                               document_number=request.data.get('document_number', None),
                                               document_expiry=request.data.get('document_expiry', None),
                                               place_of_issue=request.data.get('place_of_issue', None),
                                               converted_pdf=request.FILES.get('converted_pdf', None))
            if shared_with:
                document.shared_with.set(shared_with)
                document.save()

            serializer = DocumentSerializer(document)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DocumentUpdateView(generics.UpdateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def update(self, request, *args, **kwargs):
        try:
            document_data = Document.objects.get(pk=kwargs['pk'])

            document_category = request.data.get('document_category', None)
            document_category = DocumentCategory.objects.get(id=document_category)
            shared_with = request.data.get('shared_with', [])
            shared_with = User.objects.filter(id__in=shared_with)

            if request.data.get('document_name', None):
                document_data.document_name = request.data.get('document_name', None)
            if request.data.get('document_category', None):
                document_data.document_category = document_category
            if request.data.get('specify_category', None):
                document_data.specify_category = request.data.get('specify_category', None)
            if request.data.get('document_number', None):
                document_data.document_number = request.data.get('document_number', None)
            if request.data.get('document_expiry', None):
                document_data.document_expiry = request.data.get('document_expiry', None)
            if request.data.get('place_of_issue', None):
                document_data.place_of_issue = request.data.get('place_of_issue', None)
            if request.FILE.get('converted_pdf', None):
                document_data.converted_pdf = request.FILE.get('converted_pdf', None)
            if request.data.get('shared_with', None):
                shared_with = request.data.get('shared_with', None)
                try:
                    shared_with = json.loads(shared_with)
                except json.JSONDecodeError:
                    shared_with = None
                shared_with = User.objects.filter(id__in=shared_with) if shared_with else None
                document_data.shared_with.set(shared_with)

            document_data.save()
            serializer = DocumentSerializer(document_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DocumentVersionListView(APIView):
    def get(self, request, document_id, format=None):
        try:
            document_versions = DocumentVersion.objects.filter(document_id=document_id)
            serializer = DocumentVersionSerializer(document_versions, many=True)
            return Response(serializer.data)
        except DocumentVersion.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DocumentDeleteView(generics.UpdateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def update(self, request, *args, **kwargs):
        print(kwargs['pk'])
        try:
            document_data = Document.objects.get(pk=kwargs['pk'])
            document_data.is_delete = True
            document_data.save()
            serializer = DocumentSerializer(document_data)
            return Response({"message": 'delete successfull'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

