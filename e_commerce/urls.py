"""e_commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from product.views import RegistrationAPIView, BlacklistTokenAPIView, SecretAPIView, ProductListView, ContactAPIView, BrandListAPIView
from orders.views import CheckAPIView
from .views import index


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', index),
    path('products', index),
    path('about', index),
    path('contacts', index),
    path('register', index),
    path('login', index),
    path('cart', index),
    

    
    path('api/', ProductListView.as_view(), name='cat'),
    path('orders', CheckAPIView.as_view(), name='orders'),
    path('contact', ContactAPIView.as_view(), name='contact'),
    path('brand', BrandListAPIView.as_view(), name='brand'),
    path('users/', include('users.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    
    path('auth/register',RegistrationAPIView.as_view(), name='register'),
    path('auth/login', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout', BlacklistTokenAPIView.as_view(), name='logout'),
    path('auth/secret', SecretAPIView.as_view(), name='secret'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)