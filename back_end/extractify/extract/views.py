import pprint
from pdf2image import convert_from_path
from pytesseract import image_to_string
from rest_framework.decorators import api_view
from .models import image, filePdf
from django.http import JsonResponse#
from typing import Tuple, Union
import re
from datetime import datetime
import os
import re
from django.conf import settings 

def convert_pdf_to_img(pdf_file):
    return convert_from_path(pdf_file)


def convert_image_to_text(file):
    text = image_to_string(file)
    return text


def get_text_from_any_pdf(pdf_file):
    images = convert_pdf_to_img(pdf_file)
    final_output = {}
    for pg, img in enumerate(images):
        final_output[pg]=convert_image_to_text(img)
    return final_output


def text_preprocess(txt):
    txt = txt.replace('\n\n', '\n').split('\n')
    #print(txt)
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
        idx_NAME = get_idx_with_2_targets(utf8_txt, "ceriié", "authentique")
        champ_de_text = utf8_txt[idx_NAME +1]
        NAME  = champ_de_text[:]
        data['NAME_ENTREPRISE' ]= NAME 
    except Exception as e:
        data['NAME_ENTREPRISE' ]= "None"

    try:
        idx_facture_date = get_idx_with_2_targets(utf8_txt, "Facture", "du")
        champ_de_text = utf8_txt[idx_facture_date]
        # print(champ_de_text)
        # print(type(champ_de_text))
        x=str(''.join(list(filter(str.isdigit, champ_de_text ))))
        date =str(x[4:8]+'-'+x[2:4]+'-'+x[0:2])
        data['facure_date' ]= date 
    except Exception as e:
        data['facure_date' ]= "None"
    #extracting facture number 
    try:
        idx_facture_num = get_idx_with_1_targets(utf8_txt, "n°")
        champ_de_text = utf8_txt[idx_facture_num]
        # print(champ_de_text)
        # print(type(champ_de_text))
        number  = 'n° ' + str(int(re.search(r'\d+', champ_de_text[:]).group()) )
        data['facure_number' ]= number 
        print('*', data)
    except Exception as e:
        print(e)
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
    print("step 1")

    #extracting nom sosiete  
    try:

        idx_NAME = get_idx_with_2_targets(utf8_txt, "ETS", "MARQUET")
        champ_de_text = utf8_txt[idx_NAME]
        NAME  = champ_de_text[:]
        data['NAME_ENTREPRISE' ]= NAME 
    except Exception as e:
        print("step 2")

        data['NAME_ENTREPRISE' ]= "None"

    try:

        idx_ACHeminement = get_idx_with_1_targets(utf8_txt, "Acheminement")
        champ_de_text = utf8_txt[idx_ACHeminement]
        ACHeminement  = champ_de_text[-14:]
        data['ACHeminement' ]= ACHeminement 
    except Exception as e:
        print("step 3")

        data['ACHeminement' ]= "None"


    # #extracting echeance  
    try:

        idx_echeance = get_idx_with_2_targets(utf8_txt, "échéance" , "le")
        print("*********aaaaaaaaaaaaaa", idx_echeance)

        champ_de_text = utf8_txt[idx_echeance]
        print("*********aaaaaaaaaaaaaa")
        print(champ_de_text)
        x=str(''.join(list(filter(str.isdigit, champ_de_text ))))
        date =str(x[4:8]+'-'+x[2:4]+'-'+x[0:2])
        data['echeance' ]= date 
        print(data)

    except Exception as e:
        print("step 4")
        print(e)
        data['echeance' ]= "None"

    return data 
#####################################
# API
#####################################
@api_view(['POST'])
def extract_cin(request):
  """
  get_text = convert_image_to_text(path_ilg)
  returns dic of the for: 
  detected data : {'identity': 
                        [
                          {'nom': 'Nothing foundccccccc', --str()
                          'prenom': 'Nothing found', --> str()
                          'date de naissance': 'Nothing found', MUST BE OF TYPE datetime()
                          'lieu de naissance': 'Nothing found', -str()
                          'CIN': 'Nothing found'}# MUST BE OF TYPE int()
                        ]
                  }
  """
  if(request.method == 'POST'):
      img = image.objects.create(photo=request.FILES['file'])
      img.save()
      path=img.photo.name
      path1=os.path.join(settings.MEDIA_ROOT,str(path))
      utf8_text = convert_image_to_text(path1)
      print("___________________________")
      print("fetting text")
      print(utf8_text)
      print("______________________________")
      print("BEGUIN EXTRACTING ] ")
      first_extraction_dict = extract_page_1(utf8_text)
      """
          #returns {
          # {'NAME_ENTREPRISE: 'ETS SARL'
          # 'facure_date': 'Facture du 16/12/2020', 
          # 'facure_number': 'n° 10121328333', 
          # 'facure_TTC': 'Facture TTC 882,25 €'}
          # }

      """
      print(" first dic:")
      print(first_extraction_dict)
      data = {
        'identity' : [
          {
            'nom': first_extraction_dict['NAME_ENTREPRISE'],
            'prenom':  first_extraction_dict['facure_number'], 
            'date de naissance': first_extraction_dict['facure_date'], 
            'lieu de naissance': first_extraction_dict['facure_TTC'], 
            'CIN': 1
          }
        ]}
      print("**************************")
      print("FINAL DATA IS HERE ", data )
      print(data)
      # data = extract_identity(path1)
      # print(100 *'*')
      # print("dic shape = ", len(data))
      
      print("Here ectract_cin api view")
      return JsonResponse({'data': data})

@api_view(['POST'])
def extract_cin2(request):
  """  returns 6 dic item : 
  detected-> data : {'identity': 
                        [
                          {'nom': 'Nothing foundccccccc', --str()
                          'prenom': 'Nothing found', --> str()
                          'date de naissance': 'Nothing found', MUST BE OF TYPE datetime()
                          'lieu de naissance': 'Nothing found', -str()
                          'CIN': 'Nothing found'}# MUST BE OF TYPE int()
                        ]
                  }
  """
  if(request.method == 'POST'):
      img = image.objects.create(photo=request.FILES['file'])
      img.save()
      path=img.photo.name
      path1=os.path.join(settings.MEDIA_ROOT,str(path))
      utf8_text = convert_image_to_text(path1)
      #print(utf8_text)
      print("______________________________")
      print("BEGUIN EXTRACTING ] ")
      first_extraction_dict = extract_page_2(utf8_text)
      """
        #returns: {
        # {'NAME_ENTREPRISE': 'ETS MARQUET', 
        # 'ACHeminement': '30001790300200', 
        # 'echeance': ' 3001/2021'}
        # }

      """
      data = {
        'identity' : [
          {
            'nom': first_extraction_dict['NAME_ENTREPRISE'],
            'prenom':  first_extraction_dict['ACHeminement'], 
            'date de naissance': first_extraction_dict['echeance'], 
            'lieu de naissance': "lieu naissance", 
            'CIN': 2
          }
        ]}
      return JsonResponse({'data': data})

def merge_dicts(dict1, dict2):
    res = {**dict1, **dict2}
    return res

@api_view(['POST'])
def extract_siret_ape(request):
    if(request.method == 'POST'):
        print("DONNE: ] HERE PROCESSING WITH ectract_siret_ape api view")

        path = ''
        if str(request.FILES.get('file')).find('.pdf') != -1 :
          file_pdf = filePdf.objects.create(photo=request.FILES.get('file'))
          file_pdf.save()
          path=file_pdf.photo.name
          path1=os.path.join(settings.MEDIA_ROOT,str(path))
          print("success uploading the file __>::file_path_path = ", path)
        else:#he is checking if the file is a pdf file or not 
          print("please enter a valid pdf file")

        
        print(f"reading {path1}, \nand found {len(get_text_from_any_pdf(path1))}pages ")

        output = get_text_from_any_pdf(path1)
        if len(output)==2:
          #pprint.pprint(output)
          print("BEGUIN EXTRACTING ] ")
          _dict_1 = extract_page_1(output[0])
          print(_dict_1)
          _dict_2 = extract_page_2(output[1])
          print(_dict_2)
          dictionnary = merge_dicts(_dict_1,_dict_2)
          
          print("****************\n**************")
          pprint.pprint(dictionnary)

          """
            detected-> data : {'identity': 
                        [
                          {'nom': 'Nothing foundccccccc', --str()
                          'prenom': 'Nothing found', --> str()
                          'date de naissance': 'Nothing found', MUST BE OF TYPE datetime()
                          'lieu de naissance': 'Nothing found', -str()
                          'CIN': 'Nothing found'}# MUST BE OF TYPE int()
                        ]
                  }
          """
          data = {
            'identity' : [
              {
                'nom': dictionnary['NAME_ENTREPRISE'],
                'prenom':  dictionnary['facure_number'], 
                'date de naissance': dictionnary['facure_date'], 
                'lieu de naissance': dictionnary['facure_TTC'], 
                'CIN': dictionnary['ACHeminement'],
                'echeance': dictionnary['echeance']
              }
            ]}
              

        return JsonResponse({'data':data})



























@api_view(['POST'])
def extract(request):
    if(request.method == 'POST'):
        print("Here ectract api view")
        img = image.objects.create(photo=request.FILES['file'])
        print('befor load')
        img.save()
        path=img.photo.name
        path1=os.path.join(settings.MEDIA_ROOT,str(path))
        data = get_adresse(path1)
        print(100 *'*')
        print(data)

        return JsonResponse({'data': data})


