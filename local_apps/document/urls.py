from django.urls import path
from .views import ReportingManagerListView, DocumentListView, SharedDocumentListView, DocumentCategoryListView, \
    DocumentCreateView, DocumentUpdateView, DocumentVersionListView, DocumentDeleteView

urlpatterns = [
    path('document-list/', DocumentListView.as_view(), name='document-list'),
    path('document-create/', DocumentCreateView.as_view(), name='document-create'),
    path('document-update/<uuid:pk>/', DocumentUpdateView.as_view(), name='document-update'),
    path('document-delete/<uuid:pk>/', DocumentDeleteView.as_view(), name='document-delete'),
    path('shared-document-list/', SharedDocumentListView.as_view(), name='shared-document-list'),
    path('reporting-manager-list/', ReportingManagerListView.as_view(), name='reporting-manager-list'),
    path('document-category-list/', DocumentCategoryListView.as_view(), name='document-category-list'),
    path('document-versions/<str:document_id>/', DocumentVersionListView.as_view(), name='document-version-list'),
]
