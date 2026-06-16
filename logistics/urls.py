from django.urls import path
from . import views

app_name = 'logistics'

urlpatterns = [
    path('', views.index, name='index'),
]
