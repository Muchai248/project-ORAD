"""
URL configuration for test_database project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from database import views
from django.conf.urls.static import static 
import os
from django.conf import settings
from django.views.generic import TemplateView
# Serve static and media files during development only
from database.views import PostViewSet, serve_pdf, upload_file, fetch_documents, qc_document


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('database.urls')),
    # path('users/', views.RegisterAPIView.as_view(), name='users'),
    path('home', TemplateView.as_view(template_name='main.html'), name='home'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('register', views.register_view, name="register"),
    path('interior.html', views.interior_view, name='interior_html'),
    path('projects.html', views.project_view, name='projects_html'),
    path('sites.html', views.sites_view, name='sites_html'),
    path('serve_pdf/<str:filename>/', serve_pdf, name='serve_pdf'),
    path('fetch', PostViewSet.as_view, name='fetch'),
    path('posts/', PostViewSet.as_view({'post': 'create_post'}), name='create_post'),
    path('upload-file/', upload_file, name='upload_file'),
    path('fetch-documents/', fetch_documents, name='fetch_documents'),
    path('qc-documents/', views.qc_document, name='qc_documents'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
