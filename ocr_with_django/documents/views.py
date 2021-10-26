from django.http.response import JsonResponse
from django.views.generic.base import View, TemplateView
from django.views.decorators.csrf import csrf_exempt

from PIL import Image, ImageFilter
from tesserocr import PyTessBaseAPI


class OcrFormView(TemplateView):
    template_name = 'documents/ocr_form.html'
ocr_form_view = OcrFormView.as_view()


class OcrView(View):
    def post(self, request, *args, **kwargs):
        print("starting reading image")
        with PyTessBaseAPI() as api:
            with Image.open(request.FILES['image']) as image:
                sharpened_image = image.filter(ImageFilter.SHARPEN)#image_filter to clarify the image
                api.SetImage(sharpened_image)#to get full text
                
                utf8_text = api.GetUTF8Text()
                print("full text", api.GetUTF8Text())
                print("transforming text to utf8 bits format")
        print("finish extraction")

        return JsonResponse({'utf8_text': utf8_text})
ocr_view = csrf_exempt(OcrView.as_view())
