from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your name",
                "autocomplete": "name",
                "class": "form-control",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Your email",
                "autocomplete": "email",
                "class": "form-control",
            }
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Tell us about your idea or inquiry",
                "rows": 5,
                "class": "form-control",
            }
        ),
    )
