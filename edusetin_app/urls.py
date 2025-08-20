from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('blogs/', views.blogs, name='blogs'),
    path('blog_details/', views.blog_details, name='blog_details'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('apply-form/', views.apply_form, name='apply-form'),
    path('country/', views.country, name='country'),
    path('country-details/', views.country_details, name='country-details'),
    path('course/', views.course, name='course'),
    path('gallery/', views.gallery, name='gallery'),
    path('course-details/', views.course_details, name='course-details'),
    path('service-details/', views.service_details, name='service-details'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'edusetin_app.views.page_404'