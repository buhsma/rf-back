from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from ssapp.mailer import send_password_reset_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

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
# @api_view(["POST"])
# @permission_classes([AllowAny])
# def reset_password(request):
#     code = "good"
#     email = request.data.get("email")
#     password = request.data.get("password")
#     if email is None or password is None:
#         return Response({"error": "Please provide both email and password"}, status=400)
#     user = User.objects.filter(email=email).first()
#     if user is None:
#         return Response({"error": "User not found"}, status=400)
#     if code == "good":
#         user.set_password(password)
#         user.save()
#         return Response({"email": user.email})
#     else:
#         return Response({"error": "Code no good"}, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def request_password_reset(request):
    email = request.data.get("email")
    user = User.objects.filter(email=email).first()
    if user is None:
        return Response({"error": "User not found"}, status=400)
    
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    reset_link = f"http://relayfox.com/reset-password/{uid}/{token}"

    send_password_reset_email(email, reset_link)
    return Response({"msg": "Password reset link has been sent to your email."})


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        if not default_token_generator.check_token(user, token):
            return Response({"error": "Token is not valid"}, status=400)
        
        password = request.data.get("password")
        if password is None:
            return Response({"error": "Please provide a new password"}, status=400)
        
        user.set_password(password)
        user.save()
        return Response({"msg": "Password has been reset."})
    
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=400)
