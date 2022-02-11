import time

import requests

from django.shortcuts import render
from django.contrib import messages

from .models import Chat
from .forms import MessageForm

TOCKEN = {'X-Tasktest-Token': 'f62cdf1e83bc324ba23aee3b113c6249'}


def send_qr_code(request):
    chat = requests.get('https://dev.wapp.im/v3/chat/spare',
                        params={'crm': 'TEST', 'domain': 'test'},
                        headers=TOCKEN)
    if chat.status_code == 200 and 'token' in chat.json().keys() and 'id' in chat.json().keys():
        requests.get(f'https://dev.wapp.im/v3/instance{chat.json()["id"]}/status',
                     headers=TOCKEN,
                     params={'token': chat.json()["token"], 'full': '1'})
        for i in range(30):
            qr_code = requests.get(f'https://dev.wapp.im/v3/instance{chat.json()["id"]}/qr_code',
                                   headers=TOCKEN,
                                   params={'token': chat.json()["token"]})
            if qr_code.text:
                break
            else:
                time.sleep(1)
        Chat.objects.create(instance_id=int(chat.json()["id"]), tocken=chat.json()["token"])
        messages.success(request, 'Ok.')
        qr_code_text = qr_code.text
    else:
        messages.error(request, f'Error. {chat.json()["error_text"] if chat.status_code == 200 else chat.status_code}')
        qr_code_text = ''
    return render(
        request,
        "sender/qr_code.html",
        {"qr_code": qr_code_text},
    )


def send_message(request):
    form = MessageForm(request.POST or None)
    if request.method == "POST":
        chat = Chat.objects.last()
        data = {
            "phone": form.data['phone'],
            "body": form.data['new_message']
        }

        message = requests.post(f'https://dev.wapp.im/v3/instance{chat.instance_id}/sendMessage',
                                headers=TOCKEN,
                                params={'token': chat.tocken},
                                data=data)
        if message.status_code == 200 and 'sent' in message.json().keys():
            messages.success(request, 'Ok. Message sent.')
        else:
            messages.error(request, 'Error. Message not sent.')
    return render(
        request,
        "sender/index.html",
        {"form": form},
    )
