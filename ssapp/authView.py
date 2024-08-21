from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def test(request):
    return JsonResponse({"answer": "yup works!"})


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({"error": "Please provide both email and password"}, status=400)
    elif User.objects.filter(email=email).exists():
        return Response({"error": "User already exists"}, status=400)
    else:
        user = User.objects.create_user(username=email, email=email, password=password)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({"error": "Please provide both email and password"}, status=400)
    user = User.objects.filter(email=email).first()
    if user is None:
        return Response({"error": "User not found"}, status=400)
    if not user.check_password(password):
        return Response({"error": "Invalid password"}, status=400)
    return Response({"email": user.email})


# placeholder pwreset
@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request):
    code = "good"
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({"error": "Please provide both email and password"}, status=400)
    user = User.objects.filter(email=email).first()
    if user is None:
        return Response({"error": "User not found"}, status=400)
    if code == "good":
        user.set_password(password)
        user.save()
        return Response({"email": user.email})
    else:
        return Response({"error": "Code no good"}, status=400)


# Create your views here.
