import time

import requests

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Chat
from .forms import MessageForm




def send_qr_code(request):
    tocken = {'X-Tasktest-Token': 'f62cdf1e83bc324ba23aee3b113c6249'}
    for i in range(5):
        chat = requests.get('https://dev.wapp.im/v3/chat/spare?crm=TEST&domain=test',
                            headers=tocken)
        if chat.status_code == 200:
            break
        else:
            time.sleep(5)
    chat_json = chat.json()
    if chat.status_code == 200 and 'token' in chat_json.keys() and 'id' in chat_json.keys():
        init = requests.get(f'https://dev.wapp.im/v3/instance{chat_json["id"]}/status?token={chat_json["token"]}&full=1',
                             headers=tocken)
        while True:
            qr_code = requests.get(f'https://dev.wapp.im/v3/instance{chat_json["id"]}/qr_code?token={chat_json["token"]}',
                                    headers=tocken)
            if qr_code.text:
                break
            else:
                time.sleep(1)
        Chat.objects.create(instance_id=int(chat_json["id"]), tocken=chat_json["token"])
        return HttpResponse(qr_code.text)
    else:
        return HttpResponse('error')


def send_message(request):
    form = MessageForm(request.POST or None)
    tocken = {'X-Tasktest-Token': 'f62cdf1e83bc324ba23aee3b113c6249'}
    chat = Chat.objects.last()
    if request.method == "POST":
        data = {
        "phone": "89872745052",
        "body": form.data['new_message']
        }
        message = requests.post(f'https://dev.wapp.im/v3/instance{chat.instance_id}/sendMessage?token={chat.tocken}',
                             headers=tocken, data=data) 
        if message.status_code == 200 and message.json()['sent']:
            return HttpResponse('ok')
        else:
            return HttpResponse('error')
    return render(
        request,
        "sender/index.html",
        {"form": form},
    )