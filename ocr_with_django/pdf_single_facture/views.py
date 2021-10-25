from django.shortcuts import render

# Create your views here.

from django.http.response import JsonResponse
from django.views.generic.base import View, TemplateView
from django.views.decorators.csrf import csrf_exempt

from PIL import Image, ImageFilter
from tesserocr import PyTessBaseAPI


class OcrFormView_pdf(TemplateView):
    template_name = 'pdf_single_facture/ocr_form_pdf.html'

ocr_form_view_for_pdf = OcrFormView_pdf.as_view()


class OcrView_pdf(View):
    def post(self, request, *args, **kwargs):
        print("starting reading image")
        with PyTessBaseAPI() as api:
            with Image.open(request.FILES['image']) as image:
                sharpened_image = image.filter(ImageFilter.SHARPEN)
                api.SetImage(sharpened_image)
                utf8_text = api.GetUTF8Text()
        print("finish extraction: OK")

        return JsonResponse({'utf8_text': utf8_text})
ocr_view_for_pdf = csrf_exempt(OcrView_pdf.as_view())


