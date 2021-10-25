from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index_pdf_single_facture'),
]