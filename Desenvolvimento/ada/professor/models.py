from django import forms

class ContatoForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(
        widget=forms.Textarea,
        min_length=10,
        max_length=300,
    )
