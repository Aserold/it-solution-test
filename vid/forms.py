from django import forms


class TextForm(forms.Form):
    text = forms.CharField(label='Введите текст', max_length=100)
