from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def blogs(request):
    return render(request, 'blogs.html')

def blog_details(request):
    return render(request, 'blog_details.html')

def apply_form(request):
    return render(request, 'apply-form.html')

def coaching_details(request):
    return render(request, 'coaching-details.html')

def coaching(request):
    return render(request, 'coaching.html')



def page_404(request, exception):
    return render(request, '404.html', status=404)
