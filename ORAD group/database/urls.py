# urls.py
import os
from django.db import router
from django.urls import include, path
from rest_framework import routers
from database.views import CustomUserViewSet, register
from database.views import  PostViewSet
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
# router.register(r'login',AuthViewSet)
# router.register(r'register', AuthViewSet)
router.register(r'fetch', PostViewSet)
router.register(r'posts',PostViewSet)
router.register(r'customuser', CustomUserViewSet)
# router.register(r'post', PostViewSet, basename='post' )
# router.register(r'users', UserViewSet, basename='users')
app_name= 'database'
urlpatterns = [
    path('', include(router.urls)),
    # path('login', AuthViewSet.as_view({'post': 'login'}), name='login'),
    # path('register', AuthViewSet.as_view({'post': 'register'}), name='register'),   
    path('auth', include('rest_framework.urls', namespace='rest_framework')),
    path('Useradmin', TemplateView.as_view(template_name='Admin.html')),
    path('home', TemplateView.as_view(template_name='main.html'), name='home'),
    # path('users/', RegisterAPIView.as_view()),    
    path ('login'  , TemplateView.as_view(template_name= 'login.html')),
    path('logout', TemplateView.as_view(template_name="logout.html")),
    path('register', register, name='register')


    # path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    # path('signup/',user_signup_view, name='user-signup'),
    # path('login/', user_login_view, name='user-login'),
    # path('upload/', upload_document, name= 'upload-document'),
    # path('documents/',get_documents, name = 'get-documents'),
  
]  + static(settings.MEDIA_URL, document_root=os.path.join(settings.BASE_DIR, 'media'))
