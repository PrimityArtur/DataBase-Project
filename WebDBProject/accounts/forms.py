from django import forms

class Login(forms.Form):
    correo = forms.CharField(label="correo", max_length=200)
    contrasena = forms.CharField(label="contrasena", max_length=200)
    
    