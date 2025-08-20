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

def contact_us(request):
    return render(request, 'contact-us.html')



def course(request):
    return render(request, 'course.html')

def course_details(request):
    return render(request, 'course-details.html')

def service_details(request):
    return render(request, 'service-details.html')


def gallery(request):
    return render(request, 'gallery.html')


def country(request):
    return render(request, 'country.html')

def country_details(request):
    return render(request, 'country-details.html')

def admin_dashboard(request):
    return render(request, 'admin_pages/admin-dashboard.html')




def page_404(request, exception):
    return render(request, '404.html', status=404)
