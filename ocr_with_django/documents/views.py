from django.http.response import JsonResponse
from django.views.generic.base import View, TemplateView
from django.views.decorators.csrf import csrf_exempt
import re
from datetime import datetime
from PIL import Image, ImageFilter
from tesserocr import PyTessBaseAPI

def text_preprocess(txt):
    txt = txt.replace('\n\n', '\n').split('\n')
    print(txt)
    return txt

def get_idx_with_2_targets(texts, target_1, target_2): #return idx of line when founding target word 
    return [idx for idx in range(len(texts)) if  target_1 in texts[idx] and target_2 in texts[idx]][0]
def get_idx_with_1_targets(texts, target):
    return [idx for idx in range(len(texts)) if  target in texts[idx]][0]


def extract_page_1(utf8_txt):
    #returns {
    # {'facure_date': 'Facture du 16/12/2020', 
    # 'facure_number': 'n° 10121328333', 
    # 'facure_TTC': 'Facture TTC 882,25 €'}

    # }
    data={}
    utf8_txt = text_preprocess(utf8_txt)

    #extracting date 
    try:
        idx_facture_date = get_idx_with_2_targets(utf8_txt, "Facture", "du")
        champ_de_text = utf8_txt[idx_facture_date]
        # print(champ_de_text)
        # print(type(champ_de_text))
        date  = champ_de_text[:-2]
        data['facure_date' ]= date 
        print('*', data)
    except Exception as e:
        data['facure_date' ]= "None"

    #extracting facture number 
    try:
        idx_facture_num = get_idx_with_1_targets(utf8_txt, "n°")
        champ_de_text = utf8_txt[idx_facture_num]
        # print(champ_de_text)
        # print(type(champ_de_text))
        number  = champ_de_text[:]
        data['facure_number' ]= number 
        print('*', data)
    except Exception as e:
        data['facure_number' ]= "None"


    #extracting TTC montant 
    try:
        idx_facture_TTC = get_idx_with_2_targets(utf8_txt, "Facture", "TTC")
        champ_de_text = utf8_txt[idx_facture_TTC]
        # print(champ_de_text)
        # print(type(champ_de_text))
        TTC  = champ_de_text[:]
        data['facure_TTC' ]= TTC 
        print('*', data)

    except Exception as e:
        data['facure_TTC' ]= "None"

    return data 

def extract_page_2(utf8_txt):
    #returns: {
    # {'NAME_ENTREPRISE': 'ETS MARQUET', 
    # 'ACHeminement': '30001790300200', 
    # 'echeance': ' 3001/2021'}
    # }
    data={}
    utf8_txt = text_preprocess(utf8_txt)

    #extracting nom sosiete  
    try:

        idx_NAME = get_idx_with_2_targets(utf8_txt, "ETS", "MARQUET")
        print("idx_NAME: ", idx_NAME)
        champ_de_text = utf8_txt[idx_NAME]
        print(champ_de_text)
        print(type(champ_de_text))
        NAME  = champ_de_text[:]
        data['NAME_ENTREPRISE' ]= NAME 
        print('*', data)
    except Exception as e:
        data['NAME_ENTREPRISE' ]= "None"

    try:

        idx_ACHeminement = get_idx_with_1_targets(utf8_txt, "Acheminement")
        print("idx_acheminement: ", idx_ACHeminement)
        champ_de_text = utf8_txt[idx_ACHeminement]
        print(champ_de_text)
        print(type(champ_de_text))
        ACHeminement  = champ_de_text[-14:]
        data['ACHeminement' ]= ACHeminement 
        print('*', data)
    except Exception as e:
        data['ACHeminement' ]= "None"


    # #extracting echeance  
    try:

        idx_echeance = get_idx_with_1_targets(utf8_txt, "Venant")
        print(idx_echeance)
        print("echeance : ", idx_echeance)
        champ_de_text = utf8_txt[idx_echeance]
        print(champ_de_text)
        print(type(champ_de_text))
        echeance_val  = champ_de_text[-10:]
        data['echeance' ]= echeance_val 
        print('*', data)
    except Exception as e:
        data['echeance' ]= "None"



    return data 


class OcrFormView(TemplateView):
    template_name = 'documents/ocr_form.html'
ocr_form_view = OcrFormView.as_view()


class OcrView(View):
    def post(self, request, *args, **kwargs):
       
        print("BEGUIN EXTRACTING ] ")
        with PyTessBaseAPI() as api:
            with Image.open(request.FILES['image']) as image:
                sharpened_image = image.filter(ImageFilter.SHARPEN)#image_filter to clarify the image
                api.SetImage(sharpened_image)#to get full text
                utf8_text = api.GetUTF8Text()
                
                print("transforming text to utf8 bits format] ")
        print("DONNE ]")
        try:
            data = extract_page_1(utf8_text)
        except Exception as e :
            pass 
        # try :
        #     data2 = extract_page_2(utf8_text)
        # except Exception as e : 
        #     pass 
        # print(dict(data.items() + data2.items()))

        #return JsonResponse(data)

        return JsonResponse({'utf8_text': str(data)})
ocr_view = csrf_exempt(OcrView.as_view())




"""


# def extract_page_1(txt):
#     data={}
    # idx_facture_date = get_idx_with_2_targets(txt, "Facture", "de")
    # print("idx_date factire: ", idx_facture_date)
    # idx_facture_numb = get_idx_with_1_targets(txt,"n" )
    # print("idx facuture number", idx_facture_numb)
    # idx_TTC = get_idx_with_1_targets(txt,"TTC" )
    # print("idx ttc", idx_TTC)

    # data["nom_client"] = 
    # data["num_facture"]=

    # data["date_echerance"]

    # data["nontant_ttc"]
    # data["acheminement"]

class OcrView(View):
    def post(self, request, *args, **kwargs):
        with PyTessBaseAPI() as api:
            with Image.open(request.FILES['image']) as image:
                sharpened_image = image.filter(ImageFilter.SHARPEN)#image_filter to clarify the image
                api.SetImage(sharpened_image)#to get full text
                utf8_text = api.GetUTF8Text()
                # utf8_text = text_preprocess(utf8_text)
                print("__________")
                # extract_page_1(utf8_text)

        return JsonResponse({'utf8_text': utf8_text})

if __name__=="__main__":
    ocr_form_view = OcrFormView.as_view()
    ocr_view = csrf_exempt(OcrView.as_view())


"""