from django import forms

class CreateNewSoport(forms.Form):
    mensaje = forms.CharField(label='descripcion del soporte',widget=forms.Textarea)

    