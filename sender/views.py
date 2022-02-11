import time

import requests

from django.shortcuts import render
from django.contrib import messages

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
        for i in range(30):
            qr_code = requests.get(f'https://dev.wapp.im/v3/instance{chat_json["id"]}/qr_code?token={chat_json["token"]}',
                                   headers=tocken)
            if qr_code.text:
                break
            else:
                time.sleep(1)
        Chat.objects.create(instance_id=int(chat_json["id"]), tocken=chat_json["token"])
        messages.success(request, 'Ok.')
        qr_code_text = qr_code.text
    else:
        messages.error(request, f'Error. {chat_json["error_text"]}')
        qr_code_text = ''
    return render(
            request,
            "sender/qr_code.html",
            {"qr_code": qr_code_text},
        )


def send_message(request):
    form = MessageForm(request.POST or None)
    if request.method == "POST":
        tocken = {'X-Tasktest-Token': 'f62cdf1e83bc324ba23aee3b113c6249'}
        chat = Chat.objects.last()
        data = {
            "phone": form.data['phone'],
            "body": form.data['new_message']
        }

        message = requests.post(f'https://dev.wapp.im/v3/instance{chat.instance_id}/sendMessage?token={chat.tocken}',
                                headers=tocken, data=data)
        print(message.json())
        if message.status_code == 200 and 'sent' in message.json().keys():
            messages.success(request, 'Ok. Message sent.')
        else:
            messages.error(request, 'Error. Message not sent.')
    return render(
        request,
        "sender/index.html",
        {"form": form},
    )
