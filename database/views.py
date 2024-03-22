from fileinput import filename
from importlib.metadata import files
from multiprocessing import context
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render

# Create your views here.

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import CustomUser
from .serializers import CustomUserSerializer, DocumentSerializer, QCDocumentSerializer

from database.models import *
from rest_framework import permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login as internal_login
from django.http import FileResponse
import os
from django.conf import settings
from django.http import JsonResponse, HttpResponseNotFound, FileResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from .models import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
import json

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # Add any additional fields as needed

        # Create a new user
        user = CustomUser.objects.create_user(email=email, password=password)
        
        # Log the user in
        internal_login(request, user)
        
        return redirect('home')  # Redi
    #    token, _ = Token.objects.get_or_create(user=user)
    # Expires in one day
    #   refresh = RefreshToken.for_user(user)
    #   return Response({
    #       "token": str(refresh.access_token)}, status=status.HTTP_201_CREATED)
    # elif request.method == "GET":
    #     return render(request, "register.html")
    return render(request, 'register.html')

# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            internal_login(request, user)
            return redirect('home')  # Redirect to home page or any other page after successful login
        
        return render(request, 'login.html', {'error_message': 'Invalid username or password.'}) 
    return render(request, 'login.html')
# logout(request)
# return HttpResponseRedirect('/login/')


def logout(request):
    return redirect("login")

@csrf_protect
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        # Extract the filename from the uploaded file
        filename = uploaded_file.name
        
        # Create a new Document object with the title set to the filename
        document = Document(title=filename, file=uploaded_file)
        document.save()

        # Return a response indicating successful upload
        return HttpResponse('File uploaded successfully')
    else:
        # Return a response with an error message if no file was provided
        return HttpResponse('No file provided', status=400)



def serve_pdf(request, filename):
    # Serve the PDF file to the client
    pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'pdf', filename)
    if os.path.exists(pdf_file_path):
        with open(pdf_file_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{filename}"'
            return response
    else:
        return HttpResponseNotFound()

def fetch_documents(request):
    if request.method == 'GET':
        # Retrieve all documents from the database
        documents = Document.objects.all()
        
        # Serialize the documents data
        serialized_documents = [{
            'title': document.title,
            'file': document.file.url,  # Assuming you want to display the file URL
            'uploaded_at': document.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')  # Format the date as needed
        } for document in documents]
        
        # Return the serialized documents as JSON response
        return JsonResponse(serialized_documents, safe=False)
    else:
        # Handle other HTTP methods if needed
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def qc_document(request):
    if request.method == 'GET':
        # Retrieve all QC documents from the database
        documents = QCDocument.objects.all()
        
        # Serialize the documents data
        serialized_documents = []
        for document in documents:
            serialized_documents.append({
                'id': document.id,
                'document': document.document.url,
                'uploaded_at': document.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        # Return the serialized documents as JSON response
        return JsonResponse(serialized_documents, safe=False)
      

class CustomUserViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUser()
    permission_classes = permissions.IsAuthenticated


def home_view(request):
    context = {}
    return render(request, "home/main.html", context)


def Admin_view(request):
    context = {}
    return render(request, "admin/Admin.html", context)


def register_view(request):
    context = {}
    return render(request, "register.html", context)


def login_view(request):
    context = {}
    return render(request, "login/login.html", context)

def interior_view(request):
    context={}
    return render (request, 'interior.html',context)

def project_view(request):
    context={}
    return render (request, 'projects.html', context)

class SiteView(TemplateView):
    template_name = 'sites.html'

    def get(self,request):
        documents_name = [] 
        files = []
        sites = Site.objects.all()
        # Get all documents in db 
        # Create folders by filtering distinct file types
        documents = Document.objects.all()
        folders = documents.values('file_type').distinct()
        for document in documents:
            file = {
                "file_type" : document.file_type,
                "file": document.file,
                "file_name": document.file.name.split('/')[1]
            }
            files.append(file)

        return render(request, self.template_name, {"sites": sites, "folders":folders,"files": files})

    def post(self, request):
        
        if 'site_name' in request.POST:
            site_name = request.POST["site_name"]
            site = Site(name=site_name)
            site.save()
            messages.success(request, 'Site succesfully cleared.')

        elif 'file' in request.FILES:
            import ipdb;ipdb.set_trace()    
            file_type = request.POST.get("fileType")
            site_id = request.POST.get("site_id")
            files = request.FILES.get("file")

        
            site = get_object_or_404(Site, id=site_id)
            document = Document(site=site,file=files,file_type=file_type,uploaded_by=request.user)
            
            document.save()
    
        return redirect('sites')


class PostViewSet(viewsets.ModelViewSet):
    """A view for the post objects."""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[permissions.AllowAny],
        url_path=r"posts",
    )
    def create_post(self, request):
        serializer = DocumentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)