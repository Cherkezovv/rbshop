from django.urls import path
from .views import  RegisterListCreate

urlpatterns = [
    path('api/register',  RegisterListCreate.as_view() , name='register'),
   
]
