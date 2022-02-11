from django import forms


class MessageForm(forms.Form):
    phone = forms.CharField(
        initial='89872745052',
        required=True
    )
    new_message = forms.CharField(required=True)
