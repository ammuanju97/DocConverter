from django.shortcuts import render, redirect, get_object_or_404
from converter.models import DocumentPDF
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseForbidden
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
import os
import pdfkit
from django.contrib.auth import login, logout
# Create your views here.

def home(request):
    return render(request, 'users/home.html')


@login_required
def dashboard(request):
    documents = DocumentPDF.objects.filter(user = request.user)
    return render(request, 'converter/dashboard.html', {'documents': documents})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],

            )
            login(request,user)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {'form': form})


def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
    return HttpResponseForbidden("invalid request")
