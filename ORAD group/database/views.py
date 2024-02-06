from django.http import HttpRequest
from django.shortcuts import redirect, render

# Create your views here.

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import CustomUser
from .serializers import CustomUserSerializer, PostSerializer

from database.models import *
from rest_framework import permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login

# from http import HTTPMethod

# class RegisterAPIView(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'register.html'

#     def get(self, request):
#         queryset = CustomUser.objects.all()
#         return Response({'profiles': queryset})

#     def post(self, request):
#         print(request)
#         print(request.data)
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             if user is not None:
#                 login(request, user)
#             # return redirect('home')
#             #    token, _ = Token.objects.get_or_create(user=user)
#             # Expires in one day
#             refresh = RefreshToken.for_user(user)
#             return Response(
#                 {"token": str(refresh.access_token)}, status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def register(request):
    print(request)
    if request.method == "POST":
        serializer = CustomUserSerializer(data=request.POST)
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = serializer.save()
        #    user.password(request.data.get('password'))
        #    user = user.save()
        #    user = authenticate(request, email=request.data.get('email'), password=request.data.get('password'))
        if user is not None:
            login(request)
            return redirect("home")
    #    token, _ = Token.objects.get_or_create(user=user)
    # Expires in one day
    #   refresh = RefreshToken.for_user(user)
    #   return Response({
    #       "token": str(refresh.access_token)}, status=status.HTTP_201_CREATED)
    elif request.method == "GET":
        return render(request, "register.html")


@api_view(["POST", "GET"])
def login(request: HttpRequest):
    if request.method != "POST":
        return render(request, "login.html")
    
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(username=email, password=password)
    
    if user is not None and user.is_active:
        login(request, user)
        user.save()
        return render(request, "home.html")
        # return Response(
        #     {"token": str(refresh.access_token)}, status=status.HTTP_200_OK
        # )
    return Response(
            {"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
        )
# logout(request)
# return HttpResponseRedirect('/login/')


@api_view(["GET", "PUT"])
def logout(request: HttpRequest):
    logout(request)
    return redirect("login")


# class AuthViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
#     @action(detail=False, methods=['POST'],
#             permission_classes=[permissions.AllowAny],
#             url_path=r'register'
#         )
#     def register(self, request):
#         if request.method == 'POST':
#             form = self.serializer_class(data=request.data)
#             if form.is_valid():
#                 user = form.save() # Save to create the user instance
#                 username = user.username
#                 password = request.data['password']
#                 user = authenticate(username=username, password=password)
#                 response = {'user_id': user.id}
#                 return Response(response)
#             else:
#                 return Response(form.errors, status=400)

#     @api_view(['GET'])
#     def login(request, format=None):
#         username = request.query_params.get('username', None)
#         password = request.query_params.get('password', None)

#         if not (username and password):
#             return Response({"error": "Missing data"}, status=400)

#         user = authenticate(username=username, password=password)
#         if user is not None:
#             # Create a token for this user
#             refresh_token = str(RefreshToken.for_user(user))
#             access_token = str(AccessToken.for_user(user))
#             response =
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'message': 'User created successfully',
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token)
#             }, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#     def get(self, request):
#         # Render the register.html template
#         context = {}
#         return render(request, 'register.html', context)

#     @action(detail=False, methods=['POST'],
#             permission_classes=[permissions.AllowAny],
#             url_path=r'login',
#         )
#     def login(self, request):
#         fullname = request.data.get('fullname')
#         password = request.data.get('password')

#         # Check if the fullname and password are valid
#         user = authenticate(fullname=fullname, password=password)

#         if user is not None:
#             # Generate token
#             refresh = RefreshToken.for_user(user)
#             return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
#         else:
#             return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# class CustomUserViewSet(viewsets.ModelViewSet):
#     """A view for the custom user model."""
#     queryset = CustomUser.objects.all().select_related('user')
#     serializer_class = CustomUserSerializer
#     permission_classes=[permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    """A view for the post objects."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[permissions.AllowAny],
        url_path=r"fetch",
    )
    def fetch_post(self, request):
        posts = Post.objects.filter(author=request.user).order_by("-published")
        context = {"posts": posts}

        # Render the main.html template with the posts data
        return render(request, "main.html", context)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[permissions.AllowAny],
        url_path=r"posts",
    )
    def create_post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def user_signup_view(request):
#     if request.method == 'POST':
#         first_name = request.data.get('first_name')
#         email = request.data.get('email')
#         password = request.data.get('password')

#         # Check if first_name or email already exists
#         if CustomUser.objects.filter(Q(first_name=first_name) | Q(email=email)).exists():
#             return Response({'error': 'First name or Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             # Create a new custom user
#             new_user = CustomUser(first_name=first_name, email=email)
#             new_user.set_password(password)
#             new_user.is_active = False
#             new_user.save()
#             return Response({'message': 'Sign-Up Successful!!'}, status=status.HTTP_201_CREATED)
#     else:
#         return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def user_login_view(request):
#     if request.method == 'POST':
#         email = request.data.get('email')
#         password = request.data.get('password')

#         user = authenticate(request, email=email, password=password)

#         if user and user.is_active:
#             login(request, user)
#             token, _ = Token.objects.get_or_create(user=user)
#             expiration_threshold = timezone.now() + timedelta(days=1)
#             if token.created < expiration_threshold:
#                 # Regenerate token if it's about to expire
#                 token.delete()
#                 token = Token.objects.create(user=user)
#                 token.created = timezone.now()
#                 token.save()
#             return Response({'token': token.key}, status=status.HTTP_200_OK)  # Return token upon successful login
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)  # Return unauthorized status if login failed
#     else:
#         return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# class UserProfileView(RetrieveAPIView):
#     serializer_class = CustomUserSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user

# @api_view(['POST'])
# def upload_document(request):
#     serializer = DocumentSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def get_documents(request):
#     documents = Document.objects.all()
#     serializer = DocumentSerializer(documents, many=True)
#     return Response(serializer.data)
