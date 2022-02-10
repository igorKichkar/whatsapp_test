from django import forms


class MessageForm(forms.Form):
    new_message = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(),
        label="",
    )
