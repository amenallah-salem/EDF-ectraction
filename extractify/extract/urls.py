from django.urls import path,include
from . import views
urlpatterns = [
    path('extract/', views.extract,name='extract'),
    path('extract_cin/', views.extract_cin,name='extract_cin'),
    path('extract_siret_ape/', views.extract_siret_ape,name='extract_siret_ape'),
    path('extract_cin2/', views.extract_cin2,name='extract_cin2'),
]
