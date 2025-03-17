from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class DocumentPDF(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    docx_file = models.FileField(upload_to='uploads/')
    pdf_file = models.FileField(upload_to='converted/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.docx_file.name}"
