from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_and_convert, name="upload_convert"),
    path("download/<int:document_id>/", views.download_pdf, name="download_pdf"),
]
