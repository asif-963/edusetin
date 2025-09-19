from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404,redirect
from .models import Country,University,Course,TeamMember,Testimonial,Blog,Service,Category,GalleryImage,ContactMessage,Application,CourseCategory,Inquiry
from django.core.paginator import Paginator
from .forms import CountryForm,UniversityForm,CourseForm,TeamMemberForm,TestimonialForm,BlogForm,ServiceForm,CategoryForm,GalleryImageForm,ContactMessageForm,ApplicationForm,CourseCategoryForm,InquiryForm
from django.contrib import messages
import math
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from openpyxl import Workbook
import csv
from django.db.models import Count
from django.db.models.functions import TruncMonth
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import ChatConversation
import json



# user side >>>>
def index(request):
    print(">>> Entering index view")
    course_categories = CourseCategory.objects.all()
    countries = Country.objects.all()

    countriess = Country.objects.order_by('-id')[:5]
    team_members = TeamMember.objects.all()[:6]
    universities = University.objects.all()
    services = Service.objects.all()
    # services = Service.objects.all()[:5] 
    testimonials = Testimonial.objects.all()[:4]
    blogs = Blog.objects.all().order_by('-created_at')[:2] 
    print(">>>>>>>>>>>>>>>>>>>>.Countries in index:", countries)
    print(">>>>>>>>>>>>>>>>>>>>.Countries in index:", team_members)
    return render(request, "index.html", {"countries": countries,"team_members":team_members,"countriess":countriess,"services":services,"universities":universities,"testimonials":testimonials,"blogs":blogs, "course_categories":course_categories} )

def inquiry_view(request):
    if request.method == "POST":
        form = InquiryForm(request.POST)
        if form.is_valid():
            # Save the form to database
            form.save()
            print(form,"this is my form>>>>>>>>>>>>>>>>>")
            messages.success(request, "Your inquiry has been submitted successfully!")
            
            # Redirect to prevent form resubmission
            return redirect("contact_us")
        else:
            # Form is invalid, show errors
            messages.error(request, "Please correct the errors below.")
    else:
        form = InquiryForm()

    categories = CourseCategory.objects.all()
    services = Service.objects.all()
    countries = Country.objects.all()

    context =  {
        "form": form,
        "categories": categories,
        "countries":countries,
        "services": services,
        }

    return render(request, "contact-us.html",context)



def country_details(request, pk):
    course_categories = CourseCategory.objects.all()
    universities = University.objects.all()
    services = Service.objects.all()
    blogs = Blog.objects.all()

    country = get_object_or_404(Country, pk=pk)
    countries = Country.objects.exclude(pk=pk)  # other countries
    
    # Get all universities for this country
    universities_list = country.universities.all().order_by("-created_at")
    
    # Pagination - 4 universities per page
    paginator = Paginator(universities_list, 4)
    page = request.GET.get('page')
    
    try:
        universities = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        universities = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        universities = paginator.page(paginator.num_pages)
    
    context = {
        'country': country,
        'countries': countries,
        'universities': universities,
        "course_categories":course_categories,
        "services":services,
        "blogs":blogs,
    }
    return render(request, 'country-details.html', context)


def university_detail(request, pk):
    course_categories = CourseCategory.objects.all()
    countries = Country.objects.all()
    universities = University.objects.all()
    
    services = Service.objects.all()
    blogs = Blog.objects.all()
    university = get_object_or_404(University, id=pk)
    courses = Course.objects.filter(university=university)
    # application_form = ApplicationForm.objects.last()
    
    # Calculate course groups (3 courses per slide)
    paginator = Paginator(courses, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    context = {
        'university': university,
        'courses': courses,
        'page_obj': page_obj, 
        "course_categories":course_categories,
        "services":services,
        "blogs":blogs,
        'countries': countries,
        "universities":universities,

         
        # "application_form": application_form
    }
    return render(request, 'university_detail.html', context)



# def course_detail(request, pk):
#     course = get_object_or_404(Course, pk=pk)
#     return render(request, "course-detail.html", {"course": course})



def about(request):
    course_categories = CourseCategory.objects.all()
    countries = Country.objects.all()
    universities = University.objects.all()
    services = Service.objects.all()
    blogs = Blog.objects.all()
    
    team_members = TeamMember.objects.all()[:6]
    testimonials = Testimonial.objects.all()[:4]

    context = {
        'universities': universities,
        "course_categories":course_categories,
        "services":services,
        "blogs":blogs,
        'countries': countries,
        'team_members':team_members,
        'testimonials':testimonials,

         
        # "application_form": application_form
    }

    return render(request, 'about.html',context)


def blog_details(request, blog_id):

    course_categories = CourseCategory.objects.all()
    countries = Country.objects.all()
    universities = University.objects.all()
    services = Service.objects.all()
   

    # Get the current blog post
    blog = get_object_or_404(Blog, id=blog_id)
    
    # Get recent blogs for sidebar (excluding current blog)
    recent_blogs = Blog.objects.exclude(id=blog_id).order_by('-created_at')[:5]
    
    # Get related blogs (you can customize this logic)
    related_blogs = Blog.objects.exclude(id=blog_id).order_by('-created_at')[:3]
    
    context = {
        'blog': blog,
        'recent_blogs': recent_blogs,
        'related_blogs': related_blogs,
         'universities': universities,
        "course_categories":course_categories,
        "services":services,
        'countries': countries,

    }
    
    return render(request, 'blog_details.html', context)


def contact_submit(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect(request.META.get("HTTP_REFERER", "/"))
        else:
            messages.error(request, "There was an error sending your message. Please try again.")
    else:
        form = ContactMessageForm()
    return render(request, "university_detail.html", {"form": form})



# Admin-side list messages (custom page)
@login_required(login_url="admin_login")
def admin_contacts(request):
    contacts = ContactMessage.objects.all().order_by("-created_at")

    # Date filter
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    if start_date and end_date:
        contacts = contacts.filter(created_at__date__range=[start_date, end_date])

    paginator = Paginator(contacts, 10)  # 10 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "admin_pages/contact_list.html", {"contacts": page_obj})

from django.urls import reverse

@login_required(login_url="admin_login")
def delete_contact(request, contact_id):
    contact = get_object_or_404(ContactMessage, id=contact_id)
    if request.method == "POST":
        contact.delete()
        messages.success(request, "Contact message deleted successfully.")
        return redirect("admin_contacts")
    messages.error(request, "Invalid request.")
    return redirect("admin_contacts")



# Export to Excel/CSV
@login_required(login_url="admin_login")
def export_contacts_excel(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    contacts = ContactMessage.objects.all()
    if start_date and end_date:
        contacts = contacts.filter(created_at__date__range=[start_date, end_date])

    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Contacts"

    # Header row
    ws.append(["Name", "Email", "Phone", "Message", "Created At"])

    # Data rows
    for c in contacts:
        ws.append([
            c.name,
            c.email,
            c.phone,
            c.message,
            c.created_at.strftime("%Y-%m-%d %H:%M"),
        ])

    # Prepare response
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="contacts_{datetime.date.today()}.xlsx"'

    wb.save(response)
    return response


def service_detail(request, pk):
    # blog = blog.objects.all()
    services = Service.objects.all()
    course_categories = CourseCategory.objects.all()
    countries = Country.objects.all()
    service = get_object_or_404(Service, pk=pk)
    
    
    context = {
        # 'blog': blog,
        "course_categories":course_categories,
        "service":service,
        'countries': countries,
        "services":services,

    }
    
    return render(request, "service_detail.html", context)


def gallery(request):
    blog = Blog.objects.all()
    course_categories = CourseCategory.objects.all()
    countries = Country.objects.all()
    services = Service.objects.all()

    categories = Category.objects.all()
    images = GalleryImage.objects.all()

    context = {
        "categories": categories,
        "images": images,
        'blog': blog,
        "course_categories":course_categories,
        "services":services,
        "countries":countries,
        

    }
    return render(request, "gallery.html",context)


@login_required(login_url="admin_login")
def admin_dashboard(request):
    # Stats
    stats = {
        "applications_count": Application.objects.count(),
        "inquiries_count": Inquiry.objects.count(),
        "countries_count": Country.objects.count(),
    }

    contacts_count = ContactMessage.objects.count()


    applications_data = (
        Application.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Testimonials per month
    testimonials_data = (
        Testimonial.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    applications_labels = [x['month'].strftime("%b %Y") for x in applications_data]
    applications_counts = [x['count'] for x in applications_data]

    testimonials_labels = [x['month'].strftime("%b %Y") for x in testimonials_data]
    testimonials_counts = [x['count'] for x in testimonials_data]
    

    # Recent Data
    recent_applications = Application.objects.select_related("course").order_by("-created_at")[:5]
    recent_inquiries = Inquiry.objects.order_by("-created_at")[:5]

    # Top Countries (by applications count)
    top_countries = (
        Country.objects.annotate(app_count=Count("application"))
        .order_by("-app_count")[:5]
    )

    context = {
        "stats": stats,
        "contacts_count": contacts_count,
        "recent_applications": recent_applications,
        "recent_inquiries": recent_inquiries,
        "top_countries": top_countries,
        "applications_labels": applications_labels,
        "applications_counts": applications_counts,
        "testimonials_labels": testimonials_labels,
        "testimonials_counts": testimonials_counts,
    }
    return render(request, "admin_pages/admin-dashboard.html", context)



def page_404(request, exception):
    return render(request, '404.html', status=404)

@login_required(login_url="admin_login")
def country_list(request):
    countries_qs = Country.objects.all()
    paginator = Paginator(countries_qs, 6)  # 10 per page
    page_number = request.GET.get('page')
    countries = paginator.get_page(page_number)
    return render(request, "admin_pages/country_list.html", {"countries": countries})

@login_required(login_url="admin_login")
def country_create(request):
    if request.method == "POST":
        form = CountryForm(request.POST, request.FILES)
        if form.is_valid():
            country = form.save()
            
            messages.success(request, "Country created successfully.")
            return redirect("country_list")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CountryForm()
    return render(request, "admin_pages/create-country.html", {"form": form})

@login_required(login_url="admin_login")
def country_update(request, pk):
    country = get_object_or_404(Country, pk=pk)
    if request.method == "POST":
        form = CountryForm(request.POST, request.FILES, instance=country)
        if form.is_valid():
            country = form.save()
            
            messages.success(request, "Country updated successfully.")
            return redirect("country_list")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CountryForm(instance=country)
    return render(request, "admin_pages/country_list.html", {"form": form, "country": country})

@login_required(login_url="admin_login")
def country_delete(request, pk):
    country = get_object_or_404(Country, pk=pk)
    if request.method == "POST":
        country.delete()
        messages.success(request, "Country deleted successfully.")
        return redirect("country_list")
    return render(request, "admin_pages/country_list.html", {"country": country})

@login_required(login_url="admin_login")
def add_university(request):
    countries = Country.objects.all()

    if request.method == "POST":
        form = UniversityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "University added successfully!")
            return redirect('uni-list')
    else:
        form = UniversityForm()

    context = {
        'form': form,
        'countries': countries
    }
    return render(request, 'admin_pages/create_university.html', context)


@login_required(login_url="admin_login")
def university_list(request):
    universities = University.objects.select_related("country").all()
    countries = Country.objects.all()  # for filter dropdown if needed

    paginator = Paginator(universities, 6)  # Show 10 countries per page
    page = request.GET.get('page')
    universities = paginator.get_page(page)

    context = {
        "universities": universities,
        "countries": countries,
    }
    return render(request, "admin_pages/university_list.html", context) 


@login_required(login_url="admin_login")
# Update university
def update_university(request, pk):
    university = get_object_or_404(University, pk=pk)
    if request.method == "POST":
        form = UniversityForm(request.POST, request.FILES, instance=university)
        if form.is_valid():
            form.save()
            messages.success(request, "University updated successfully!")
            return redirect("uni-list")
    else:
        form = UniversityForm(instance=university)

    context = {"form": form, "university": university}
    return render(request, "admin_pages/update_university.html", context)

@login_required(login_url="admin_login")
#  Delete university
def delete_university(request, pk):
    university = get_object_or_404(University, pk=pk)
    if request.method == "POST":  # confirmation before delete
        university.delete()
        messages.success(request, "University deleted successfully!")
        return redirect("uni-list")

    context = {"university": university}
    return render(request, "admin_pages/delete_university.html", context)


@login_required(login_url="admin_login")
def course_list(request):
    courses_qs = Course.objects.select_related("university__country").all().order_by("-id")

    # paginate (10 courses per page, you can change the number)
    paginator = Paginator(courses_qs, 6)
    page_number = request.GET.get("page")
    courses = paginator.get_page(page_number)  # this gives you a Page object

    universities = University.objects.select_related("country").all()

    return render(request, "admin_pages/course_list.html", {
        "courses": courses,            # now a Page object, works with your template
        "universities": universities,
    })

@login_required(login_url="admin_login")
# Add new course
def course_add(request):

    categories = CourseCategory.objects.all().order_by("-created_at")
    print("ebtererrere")
    if request.method == "POST":
        form = CourseForm(request.POST,request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, "Course added successfully!")
            return redirect("course_list")  # update with your course list url name
        
    else:
        form = CourseForm()
        
    universities = University.objects.select_related("country").all()

    
    return render(request, "admin_pages/course_create.html", {"form": form, "universities":universities,"categories":categories}) 

@login_required(login_url="admin_login")
#  Update course
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    universities = University.objects.select_related("country").all()  # Get all universities
    categories = CourseCategory.objects.all().order_by("-created_at")
    print(categories)

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully!")
            return redirect("course_list")
    else:
        form = CourseForm(instance=course)

    # In case of form errors, we need to render the course_list template with the form and the universities
    courses = Course.objects.select_related("university__country").all()  
    return render(
        request,
        "admin_pages/course_list.html",
        {
            "form": form,
            "course": course,  
            "courses": courses, 
            "universities": universities,  # pass to template
            "categories": categories,
        }
    )

@login_required(login_url="admin_login")
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        course.delete()
        messages.success(request, "Course deleted successfully!")
        return redirect("course_list")
    return render(request, "admin_pages/course_list.html", {"course": course})




@csrf_exempt
def ckeditor_upload(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        upload = request.FILES['upload']
        file_extension = os.path.splitext(upload.name)[1].lower()
        
        # Check if the uploaded file is an image or a PDF
        if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            folder = 'images'
        elif file_extension == '.pdf':
            folder = 'pdfs'
        else:
            return JsonResponse({'uploaded': False, 'error': 'Unsupported file type.'})

        # Save the file in the appropriate folder
        file_name = default_storage.save(f'{folder}/{upload.name}', ContentFile(upload.read()))
        file_url = default_storage.url(file_name)
        return JsonResponse({
            'uploaded': True,
            'url': file_url
        })
    
    return JsonResponse({'uploaded': False, 'error': 'No file was uploaded.'})


@login_required(login_url="admin_login")
def list_team(request):
    """Display all team members with pagination"""
    team_members_list = TeamMember.objects.all().order_by('name')
    paginator = Paginator(team_members_list, 6)  # Show 10 per page
    page_number = request.GET.get('page')
    team_members = paginator.get_page(page_number)  # handles invalid pages automatically

    context = {
        'team_members': team_members,
        'title': 'Team Members',
    }
    return render(request, 'admin_pages/team_list.html', context)


@login_required(login_url="admin_login")
def create_team(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member added successfully!')
            return redirect('team_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = TeamMemberForm()

    return render(request, 'admin_pages/add_team.html', {'form': form})


@login_required(login_url="admin_login")
def edit_team_member(request, pk):
    team_member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES, instance=team_member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member updated successfully!')
            return redirect('team_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeamMemberForm(instance=team_member)
    
    return render(request, 'admin_pages/edit_team_member.html', {
        'form': form,
        'team_member': team_member
    })


@login_required(login_url="admin_login")
def delete_team_member(request, pk):
    team_member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        team_member.delete()
        messages.success(request, 'Team member deleted successfully!')
        return redirect('team_list')
    
    return render(request, 'admin_pages/confirm_delete.html', {'team_member': team_member})


@login_required(login_url="admin_login")
def testimonial_list(request):
    testimonials = Testimonial.objects.all()
    return render(request, "admin_pages/review_list.html", {"testimonials": testimonials})


@login_required(login_url="admin_login")
def testimonial_list(request):
    testimonials_list = Testimonial.objects.all().order_by('name') 
    paginator = Paginator(testimonials_list, 6)  # 10 testimonials per page
    page_number = request.GET.get('page')
    testimonials = paginator.get_page(page_number)  # returns a Page object

    return render(request, "admin_pages/review_list.html", {"testimonials": testimonials})

@login_required(login_url="admin_login")
def testimonial_create(request):
    if request.method == "POST":
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial added successfully!")
            return redirect("testimonial_list")
    else:
        form = TestimonialForm()
    return render(request, "admin_pages/create_review.html", {"form": form})

@login_required(login_url="admin_login")
def testimonial_update(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial updated successfully!")
            return redirect("testimonial_list")
    else:
        form = TestimonialForm(instance=testimonial)
    return render(request, "testimonials/testimonial_form.html", {"form": form, "testimonial": testimonial})

@login_required(login_url="admin_login")
def testimonial_delete(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        testimonial.delete()
        messages.success(request, "Testimonial deleted successfully!")
        return redirect("testimonial_list")
    return render(request, "testimonials/testimonial_confirm_delete.html", {"testimonial": testimonial})



# --------- Services ---------
@login_required(login_url="admin_login")
def service_list(request):
    services_list = Service.objects.all().order_by('title') 
    paginator = Paginator(services_list, 6)  # 10 services per page
    page_number = request.GET.get('page')
    services = paginator.get_page(page_number)  # returns a Page object

    return render(request, "admin_pages/service_list.html", {"services": services})

@login_required(login_url="admin_login")
def service_create(request):
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service added successfully!")
            return redirect("service_list")
    else:
        form = ServiceForm()
    return render(request, "admin_pages/create_service.html", {"form": form})

@login_required(login_url="admin_login")
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully!")
            return redirect("service_list")
    else:
        form = ServiceForm(instance=service)
    return render(request, "admin_pages/service_list.html", {"form": form, "service": service})



@login_required(login_url="admin_login")
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        service.delete()
        messages.success(request, "Service deleted successfully!")
        return redirect("service_list")
    
    # If it's a GET request, show confirmation (handled by the modal)
    return redirect("service_list")


# --------- Blogs ---------
@login_required(login_url="admin_login")
def blog_list(request):
    blogs_qs = Blog.objects.all().order_by("-id")  # newest first

    paginator = Paginator(blogs_qs, 6)  # show 10 blogs per page
    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)  # gives a Page object

    return render(request, "admin_pages/blog_list.html", {
        "blogs": blogs
    })


@login_required(login_url="admin_login")
def blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog added successfully!")
            return redirect("blog_list")
    else:
        form = BlogForm()
    return render(request, "admin_pages/create_blog.html", {"form": form})


@login_required(login_url="admin_login")
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated successfully!")
            return redirect("blog_list")
    else:
        form = BlogForm(instance=blog)
    return render(request, "admin_pages/create_blog.html", {"form": form, "blog": blog})


@login_required(login_url="admin_login")
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog deleted successfully!")
        return redirect("blog_list")
    return render(request, "admin_pages/create_blog.html", {"blog": blog})



@login_required(login_url="admin_login")
def gallery_images(request):
    categories = Category.objects.all().prefetch_related("images")

    category_pages = {}
    for category in categories:
        images_qs = category.images.all().order_by("-uploaded_at")
        paginator = Paginator(images_qs, 8)  # 8 images per page
        page_number = request.GET.get(f'page_{category.id}', 1)
        
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
            
        category_pages[category.id] = page_obj

    return render(request, "admin_pages/image_list.html", {
        "categories": categories,
        "category_pages": category_pages,
    })



@login_required(login_url="admin_login")
def add_image(request):
    categories = Category.objects.all()
    
    if request.method == "POST":
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)
        files = request.FILES.getlist("images")
        print("FILES:", request.FILES)  # Should show uploaded files
        print("FILES count:", len(request.FILES.getlist("images")))

        for file in files:
            GalleryImage.objects.create(
                category=category,
                title=file.name,   # default title = filename
                image=file
            )
        messages.success(request, "Images uploaded succesfully")
        return redirect("list_image")
    return render(request, "admin_pages/add_image.html", {"categories": categories})



@login_required(login_url="admin_login")
def upload_application_form(request):
    if request.method == "POST":
        title = request.POST.get("title")
        pdf = request.FILES.get("pdf")

        if pdf and pdf.name.endswith(".pdf"):
            ApplicationForm.objects.create(title=title, pdf=pdf)
            messages.success(request, "Application form successfully!")
            return redirect("upload_application_form")  # reload page

    forms = ApplicationForm.objects.all()
    return render(request, "admin_pages/add_application_form.html", {"forms": forms})


def apply_form(request):
    countries = Country.objects.all()
    courses = Course.objects.all()

    course_categories = CourseCategory.objects.all().order_by("name")
    services = Service.objects.all()

    if request.method == "POST":
        form = ApplicationForm(request.POST)  # ✅ include FILES
        if form.is_valid():
            form.save()
            messages.success(request, "Your application has been submitted successfully!")
            return redirect("apply_form")  # make sure you have `path("apply/", views.apply_form, name="apply_form")`
        else:
            messages.error(request, "❌ Please correct the errors below.")
    else:
        form = ApplicationForm()

    context = {
        "form": form,
        "countries": countries,
        "courses": courses,
        "course_categories":course_categories,
        "services":services,

    }
    return render(request, "apply-form.html", context)


@login_required(login_url="admin_login")
def application_list(request):
    apps = Application.objects.all().order_by("-created_at")
   

    # Date filter
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    if start_date and end_date:
        apps = apps.filter(created_at__date__range=[start_date, end_date])

    # Pagination
    paginator = Paginator(apps, 10)  # 10 per page
    page = request.GET.get("page")
    applications = paginator.get_page(page)

    return render(request, "admin_pages/application_list.html", {
        "applications": applications,
    })



def delete_application(request, app_id):
    app = get_object_or_404(Application, id=app_id)
    if request.method == "POST":
        app.delete()
        messages.success(request, "Application deleted successfully.")
        return redirect("application_list")
    messages.error(request, "Invalid request.")
    return redirect("application_list")



def get_courses_by_country(request, country_id):
    courses = Course.objects.filter(university__country_id=country_id).values("id", "title")
    return JsonResponse(list(courses), safe=False)


@login_required(login_url="admin_login")
def course_category_list_create(request):
    categories = CourseCategory.objects.all().order_by("-created_at")

    if request.method == "POST":
        form = CourseCategoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Category added successfully!")
            return redirect("course_category_list")
    else:
        form = CourseCategoryForm()

    context = {
        "categories": categories,
        "form": form,
    }
    return render(request, "admin_pages/course_category.html", context)



@login_required(login_url="admin_login")
def export_applications_excel(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    applications = Application.objects.all()
    if start_date and end_date:
        applications = applications.filter(created_at__date__range=[start_date, end_date])

    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Applications"

    # Header row
    ws.append([
        "Full Name",
        "Email",
        "Phone",
        "Qualification",
        "Marks",
        "Course",
        "Country",
        "Created At"
    ])

    # Data rows
    for app in applications:
        ws.append([
            app.full_name,
            app.email,
            app.phone,
            app.qualification or "",
            float(app.marks) if app.marks else "",
            app.course.title if app.course else "",  # ✅ corrected here
            app.country.name if app.country else "",
            app.created_at.strftime("%Y-%m-%d %H:%M"),
        ])

    # Prepare response
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="applications_{datetime.date.today()}.xlsx"'

    wb.save(response)
    return response




def course_category_detail(request, category_id):
    categories = CourseCategory.objects.all().order_by('name')  
    category = get_object_or_404(CourseCategory, id=category_id)
    courses = Course.objects.filter(category=category).order_by("-id")
    countries = Country.objects.all()
    services = Service.objects.all()

    # Paginate courses
    paginator = Paginator(courses, 4)  # 4 courses per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "category": category,
        "page_obj": page_obj, 
        "courses":courses,
        "category":category, # use this in template
        "categories":categories,
        "countries":countries,
        "services":services,
    }
    return render(request, "category_detials.html", context)

@login_required(login_url="admin_login")
def course_category_list(request):
    categories = CourseCategory.objects.all().order_by('name')  # order by name like in model Meta

    # Pagination
    paginator = Paginator(categories, 10)  # 10 categories per page
    page_number = request.GET.get('page')
    categories_page = paginator.get_page(page_number)

    context = {
        'categories': categories_page,
    }
    return render(request, 'admin_pages/course_category_list.html', context)

@login_required(login_url="admin_login")
def course_category_update(request, pk):
    category = get_object_or_404(CourseCategory, pk=pk)
    if request.method == 'POST':
        form = CourseCategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Category updated successfully!")
            return redirect('course_category_list')
    else:
        form = CourseCategoryForm(instance=category)
    return render(request, 'admin_pages/course_category_update.html', {'form': form, 'category': category})

@login_required(login_url="admin_login")
def course_category_delete(request, pk):
    category = get_object_or_404(CourseCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "✅ Category deleted successfully!")
        return redirect('course_category_list')
    return render(request, 'admin_pages/course_category_delete.html', {'category': category})


def index_blog(request):
    blogs = Blog.objects.all().order_by('-created_at')

    course_categories = CourseCategory.objects.all().order_by("name")
    countries = Country.objects.all()
    services = Service.objects.all()
    paginator = Paginator(blogs, 2)  # 2 blogs per page
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    context={
        "course_categories": course_categories,
        "page_obj": page_obj, 
        "countries":countries,
        "services":services,
    }

    return render(request, 'blogs.html', context)



@login_required(login_url="admin_login")
def delete_image(request, image_id):
    image = get_object_or_404(GalleryImage, id=image_id)
    
    if request.method == "POST":
        image.delete()
        messages.success(request, "Image deleted successfully")
        return redirect("list_image")

    return render(request, "admin_pages/image_list.html", {"image": image})


@login_required(login_url="admin_login")
def category_list(request):
    categories = Category.objects.all().order_by("-created_at")
    paginator = Paginator(categories, 10)
    page_number = request.GET.get("page")
    categories = paginator.get_page(page_number)
    return render(request, "admin_pages/category_list.html", {"categories": categories})

@login_required(login_url="admin_login")
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Category.objects.create(name=name)
            return redirect("category_list")
    return render(request, "admin_pages/add_category.html")

@login_required(login_url="admin_login")
def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.name = request.POST.get("name")
        category.save()
        return redirect("category_list")
    return redirect("category_list")

@login_required(login_url="admin_login")
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        return redirect("category_list")
    return redirect("category_list")



@login_required(login_url="admin_login")
def inquiry_list(request):
    inquiries = Inquiry.objects.all().order_by('-created_at')
    
    # Date filtering
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date:
        inquiries = inquiries.filter(created_at__date__gte=start_date)
    if end_date:
        inquiries = inquiries.filter(created_at__date__lte=end_date)
    
    # Pagination
    paginator = Paginator(inquiries, 7)  # Show 20 inquiries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'inquiries': page_obj,
    }
    return render(request, 'admin_pages/inquiry_list.html', context)


@login_required(login_url="admin_login")
def delete_inquiry(request, pk):
    inquiry = get_object_or_404(Inquiry, pk=pk)
    if request.method == "POST":
        inquiry.delete()
        return redirect('inquiry_list')  # change to your listing view name
    return redirect('inquiry_list')


import pandas as pd

@login_required(login_url="admin_login")
def export_inquiries_excel(request):
    # Get filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    # Filter inquiries based on date range
    inquiries = Inquiry.objects.all()
    
    if start_date:
        inquiries = inquiries.filter(created_at__date__gte=start_date)
    if end_date:
        inquiries = inquiries.filter(created_at__date__lte=end_date)
    
    # Prepare data for Excel
    data = []
    for inquiry in inquiries:
        data.append({
            'Name': inquiry.name,
            'Email': inquiry.email,
            'Phone': inquiry.phone if inquiry.phone else '-',
            'Message': inquiry.message,
            'Date': inquiry.created_at.strftime("%Y-%m-%d %H:%M")
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create HTTP response with Excel file
    response = HttpResponse(content_type='application/ms-excel')
    filename = f"contact_inquiries_{timezone.now().strftime('%Y%m%d_%H%M')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Write DataFrame to Excel
    df.to_excel(response, index=False, sheet_name='Contact Inquiries')
    
    return response


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "Both fields are required.")
            return render(request, "authenticate/login.html")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:   # ✅ only staff users
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            print("login sucesfull")
            return redirect("admin-dashboard")  # change this to your dashboard URL
        else:
            messages.error(request, "Invalid credentials or not an admin.")

    return render(request, "authenticate/login.html")


@login_required(login_url="admin_login")
def admin_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("admin_login")


@csrf_exempt
def save_user_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            conv = ChatConversation.objects.create(
                name=data.get("name"),
                course=data.get("course"),
                subject=data.get("subject"),
                year_of_passing=data.get("year"),
                # user_message=data.get("user_message"),
                # bot_response=data.get("bot_response")
            )
            print(conv,'ths detilssss>>>>>>>>>>>>>>>>')

            return JsonResponse({"status": "success", "id": conv.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=405)