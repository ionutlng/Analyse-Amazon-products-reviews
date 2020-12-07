from django.urls import path
from . import views

app_name = 'interface'

urlpatterns = [
    path('search_item/', views.index, name='search_item'),
]
