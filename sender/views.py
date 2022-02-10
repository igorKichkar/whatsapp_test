import time
from django.http import HttpResponse

import requests


def send_message(request):
    tocken = {'X-Tasktest-Token': 'f62cdf1e83bc324ba23aee3b113c6249'}
    for i in range(5):
        chat = requests.get('https://dev.wapp.im/v3/chat/spare?crm=TEST&domain=test',
                            headers=tocken)
        if chat.status_code == 200:
            break
        else:
            time.sleep(5)
    chat_json = chat.json()
    print(chat_json)
    if chat.status_code == 200 and 'token' in chat_json.keys() and 'id' in chat_json.keys():
        init = requests.get(f'https://dev.wapp.im/v3/instance{chat_json["id"]}/status?token={chat_json["token"]}&full=1',
                             headers=tocken)
        qr_code = requests.get(f'https://dev.wapp.im/v3/instance{chat_json["id"]}/qr_code?token={chat_json["token"]}',
                               headers=tocken)
        
        return HttpResponse(qr_code.text)
    else:
        return HttpResponse('error')
