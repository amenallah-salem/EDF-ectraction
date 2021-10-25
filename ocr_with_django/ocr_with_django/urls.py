"""ocr_with_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from documents.views import ocr_view, ocr_form_view
from pdf_single_facture.views import ocr_form_view_for_pdf, ocr_view_for_pdf

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ocr/', ocr_view, name='ocr_view'),
    url(r'^$', ocr_form_view, name='ocr_form_view'),
    #second app :: odf single_facture 
    #path('pdf_single_facture/', include('pdf_single_facture.urls')),
    url(r'^ocr_for_pdf/', ocr_view_for_pdf, name='ocr_view_for_pdf'),
    url(r'^for_pdf/', ocr_form_view_for_pdf, name='ocr_form_view_for_pdf'),

]
