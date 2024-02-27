from django.urls import path
from .views import user_api
from .views import userAccountActivate


urlpatterns = [
    path('user/',user_api),
    path('activate/<uid>/<token>/',userAccountActivate,name='activate'),
]