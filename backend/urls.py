"""
URL configuration for backend project.

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
from django.urls import path
from ssapp.contactView import contactRelay
from ssapp.authView import test, register, login, reset_password, request_password_reset
from ssapp.storageView import handleFileUpload, handleFileDownload, deleteFile, handleSecretUpload , handleSecretDownload, deleteSecret
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/test', test, name='test'),
    path('api/register', register, name='register'),
    path('api/login', login, name='login'),
    path('api/reset_password/<uidb64>/<token>/', reset_password, name='reset_password'),
    path('api/reset_password/', request_password_reset, name='request_password_reset'),
    path('api/contact', contactRelay, name='contact'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    path('api/upload/', handleFileUpload, name='upload'),
    path('api/secretup/', handleSecretUpload , name='secret'),
    path('api/download/<str:id>/<str:index>/', handleFileDownload, name='download'),
    path('api/secret/<str:id>/', handleSecretDownload, name='secret'),
    path('api/confirm/<str:id>/', deleteFile, name='confirm'),
    path('api/delete/<str:id>/', deleteSecret, name='delete'),
]
