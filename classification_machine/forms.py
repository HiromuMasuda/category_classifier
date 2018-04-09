from django import forms


class UrlForm(forms.Form):
    url = forms.CharField(label='url', max_length=100)
