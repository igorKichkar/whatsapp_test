from django.urls import path
from sender.views import send_qr_code, send_message

app_name = "sender"

urlpatterns = [
    path('', send_qr_code, name='send_qr_code'),
    path('send_message/', send_message, name='send_message')
]