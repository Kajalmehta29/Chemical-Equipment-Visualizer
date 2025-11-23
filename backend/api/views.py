import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, permissions
from rest_framework.authentication import BasicAuthentication
from django.http import HttpResponse
from django.shortcuts import get_object_or_404 
from reportlab.pdfgen import canvas
from .models import UploadedDataset
from .serializers import DatasetSerializer

def calculate_summary(file_path):
    df = pd.read_csv(file_path)
    return {
        "total_count": int(df.shape[0]),
        "averages": df.select_dtypes(include='number').mean().to_dict(),
        "type_distribution": df['Type'].value_counts().to_dict() if 'Type' in df.columns else {},
        "preview": df.head(5).to_dict(orient='records')
    }

class UploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file_serializer = DatasetSerializer(data=request.data)
        if file_serializer.is_valid():
            obj = file_serializer.save(filename=request.data['file'].name)
            
            try:
                summary = calculate_summary(obj.file.path)
                summary['filename'] = obj.filename
                return Response(summary, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"Analysis failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HistoryView(APIView):
    def get(self, request):
        last_5 = UploadedDataset.objects.order_by('-uploaded_at')[:5]
        serializer = DatasetSerializer(last_5, many=True)
        return Response(serializer.data)

class AnalysisView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        dataset = get_object_or_404(UploadedDataset, pk=pk)
        try:
            summary = calculate_summary(dataset.file.path)
            summary['filename'] = dataset.filename
            return Response(summary)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

class PDFReportView(APIView):
    def get(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="chemical_report.pdf"'
        p = canvas.Canvas(response)
        
        p.setFont("Helvetica-Bold", 18)
        p.drawString(50, 800, "Chemical Equipment Parameter Report")
        p.line(50, 790, 550, 790)
        
        last_upload = UploadedDataset.objects.last()
        
        if last_upload:
            try:
                p.setFont("Helvetica", 12)
                p.drawString(50, 760, f"Analysis of File: {last_upload.filename}")
                p.drawString(50, 745, f"Date Uploaded: {last_upload.uploaded_at.strftime('%Y-%m-%d %H:%M')}")
                
                df = pd.read_csv(last_upload.file.path)
                
                y_position = 700
                p.setFont("Helvetica-Bold", 14)
                p.drawString(50, y_position, "1. Overview")
                y_position -= 20
                p.setFont("Helvetica", 12)
                p.drawString(70, y_position, f"Total Equipment Count: {len(df)}")
                y_position -= 40
                
                p.setFont("Helvetica-Bold", 14)
                p.drawString(50, y_position, "2. Parameter Averages")
                y_position -= 20
                p.setFont("Helvetica", 12)
                
                averages = df.select_dtypes(include='number').mean().to_dict()
                for param, value in averages.items():
                    p.drawString(70, y_position, f"- Average {param}: {value:.2f}")
                    y_position -= 20
                
                y_position -= 20
                p.setFont("Helvetica-Bold", 14)
                p.drawString(50, y_position, "3. Equipment Type Distribution")
                y_position -= 20
                p.setFont("Helvetica", 12)
                
                if 'Type' in df.columns:
                    counts = df['Type'].value_counts().to_dict()
                    for etype, count in counts.items():
                        p.drawString(70, y_position, f"- {etype}: {count}")
                        y_position -= 20
                        
            except Exception as e:
                p.drawString(50, 700, f"Error reading file data: {str(e)}")
        else:
            p.drawString(50, 700, "No datasets have been uploaded yet.")
            
        p.showPage()
        p.save()
        return response