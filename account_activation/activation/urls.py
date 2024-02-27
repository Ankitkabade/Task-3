from django.urls import path
from .views import create_api,details_api


urlpatterns =[
    path('create/', create_api),
    path('details/<int:pk>/',details_api)
]