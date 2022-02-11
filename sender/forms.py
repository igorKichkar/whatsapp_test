from django import forms


class MessageForm(forms.Form):
    phone = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(),
        label="phone",
    )
    new_message = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(),
        label="message",
    )
