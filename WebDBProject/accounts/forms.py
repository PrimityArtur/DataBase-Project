from django import forms

class Login(forms.Form):
    correo = forms.CharField(label="correo", max_length=200)
    contrasena = forms.CharField(label="contrasena", max_length=200)
    

class Register(forms.Form):
    correo = forms.CharField(label="correo", max_length=100)
    contrasena = forms.CharField(label="contrasena", max_length=100)

    nombre = forms.CharField(label="nombre", max_length=200)
    apellido = forms.CharField(label="apellido", max_length=200)

    direccion = forms.CharField(label="direccion", max_length=200, required=False)
    telefono = forms.CharField(label="telefono", max_length=200, required=False)
    
    