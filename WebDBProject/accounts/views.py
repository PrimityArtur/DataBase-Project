from django.shortcuts import redirect, render #render para ir a un html, y redirect  para redireccionar a un html
from django.http import HttpResponse, JsonResponse
from django.db import connection #para optener cursor y realizar consultas SQL
# from .forms import CreateNewSoport

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')