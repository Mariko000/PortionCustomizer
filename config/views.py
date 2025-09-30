#project root config/views.py

from django.shortcuts import render

def about_page(request):
    return render(request, 'about.html')

def explained_design(request):
    return render(request, 'explained_design.html')

def my_skills(request):
    return render(request, 'my_skills.html')