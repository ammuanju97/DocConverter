from django.shortcuts import render, redirect, get_object_or_404
from .models import DocumentPDF
from.forms import DocumentForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
import os
import pdfkit
import pythoncom
from docx import Document
from comtypes.client import CreateObject
from win32com.client import Dispatch
from django.contrib import messages
# Create your views here.

@login_required
def upload_and_convert(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            docx_path = document.docx_file.path
            pdf_path = os.path.splitext(docx_path)[0] + ".pdf"

            convert_docx_to_pdf(docx_path, pdf_path)

            # pdfkit.from_file(document.docx_file.path, pdf_path)
            document.pdf_file = pdf_path
            document.save()
         
            # Redirect to the user dashboard after conversion
            return redirect('dashboard')
        # Redirect to the download page after conversion
            # return redirect('download_pdf', document.id)
    
    else:
        form = DocumentForm()
    return render(request, 'converter/upload.html', {'form' : form})


def convert_docx_to_pdf(docx_path, pdf_path):
    
    pythoncom.CoInitialize()  
    word = Dispatch('Word.Application')
    word.Visible = False

    doc = word.Documents.Open(docx_path)
    doc.SaveAs(pdf_path, FileFormat=17)  
    doc.Close()
    word.Quit()


@login_required
def download_pdf(request, document_id):

    document = get_object_or_404(DocumentPDF, id=document_id, user=request.user) 

    if not document.pdf_file:
        return HttpResponse("PDF not found.", status=404)

    return FileResponse(open(document.pdf_file.path, 'rb'), content_type='application/pdf', as_attachment=True)
