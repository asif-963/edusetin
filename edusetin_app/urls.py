from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('blogs/', views.blogs, name='blogs'),
    path('blog_details/', views.blog_details, name='blog_details'),
    path('apply-form/', views.apply_form, name='apply-form'),
    path('coaching/', views.coaching, name='coaching'),
    path('coaching-details/', views.coaching_details, name='coaching-details'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'edusetin_app.views.page_404'