import time

import requests

from django.shortcuts import render
from django.contrib import messages

from .models import Chat
from .forms import MessageForm

TOKEN = {'X-Tasktest-Token': 'f62cdf1e83bc324ba23aee3b113c6249'}


def send_qr_code(request):
    chat = requests.get('https://dev.wapp.im/v3/chat/spare',
                        params={'crm': 'TEST', 'domain': 'test'},
                        headers=TOKEN)
    if chat.status_code == 200:
        if 'error_code' in chat.json():
            messages.error(request, f'Error. {chat.json()["error_text"]}')
            return render(
                request,
                "sender/qr_code.html",
                {"qr_code": ''},
            )
        chat_data = chat.json()
        requests.get(f'https://dev.wapp.im/v3/instance{chat_data["id"]}/status',
                     headers=TOKEN,
                     params={'token': chat_data["token"], 'full': '1'})
        for i in range(30):
            qr_code = requests.get(f'https://dev.wapp.im/v3/instance{chat_data["id"]}/qr_code',
                                   headers=TOKEN,
                                   params={'token': chat_data["token"]})
            if qr_code.text:
                break
            time.sleep(1)
        Chat.objects.create(instance_id=int(chat_data["id"]), tocken=chat_data["token"])
        messages.success(request, 'Ok.')
        qr_code_text = qr_code.text
    else:
        messages.error(request, f'Error. {chat.status_code}')
        qr_code_text = ''
    return render(
        request,
        "sender/qr_code.html",
        {"qr_code": qr_code_text}
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
                                headers=TOKEN,
                                params={'token': chat.tocken},
                                data=data)
        if message.status_code == 200 and 'sent' in message.json():
            messages.success(request, 'Ok. Message sent.')
        else:
            messages.error(request, 'Error. Message not sent.')
    return render(
        request,
        "sender/index.html",
        {"form": form},
    )
