from django import forms


class MessageForm(forms.Form):
    new_message = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Dweet something..." 
            }
        ),
        label="",
    )
