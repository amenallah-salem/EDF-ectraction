#the weights are stored in google drive 
#taken from this StackOverflow answer: https://stackoverflow.com/a/39225039
import requests
import os

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


if __name__=="__main__":
    douwnload_dict={
        '1RpukbVXRA7ladm0oHx1ltxpLyJeuP-EB':'last_checkpoint',
        '1tKGDAodh8TWAyH8NMOGyBK_tI37vgvHG':'metrics.json',
        '19W26WVocv6w82SPKexUcDPUjNQABCray':'model_final.pth'
    }


    file_id=[]
    file_names=[]

    for key, val in douwnload_dict.items():
        file_id.append(key)
        file_names.append(val)
    print("file_names: {} ".format(file_names))
    print("files_ids : {}".format(file_id))
    os.mkdir("output")
    #file_id = ['1RpukbVXRA7ladm0oHx1ltxpLyJeuP-EB','1tKGDAodh8TWAyH8NMOGyBK_tI37vgvHG','19W26WVocv6w82SPKexUcDPUjNQABCray']
    #file_names=['last_checkpoint','metrics.json','model_final.pth']
    for x in range(len(file_id)):
	#in this file we will download weights within the output folder named output 
        print("start downloading {}".format(file_names[x]))
        destination = os.path.join(os.getcwd(),"output",file_names[x])
        download_file_from_google_drive(file_id[x], destination)
        print('donne downloading {}.'.format(file_names[x]))

    print('Finished downloading all files.')
