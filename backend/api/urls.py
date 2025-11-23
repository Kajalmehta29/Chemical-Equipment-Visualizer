from django.urls import path
from .views import UploadView, HistoryView, PDFReportView, AnalysisView

urlpatterns = [
    path('upload/', UploadView.as_view()),
    path('history/', HistoryView.as_view()),
    path('history/<int:pk>/', AnalysisView.as_view()), 
    path('report/', PDFReportView.as_view()),
]