from django.shortcuts import render
from django.db import connection

def home(request):
    print(connection.settings_dict)
    return render(request, "portal/home.html")