from django import forms

class CreateNewSoport(forms.Form):
    mensaje = forms.CharField(label='descripcion del soporte',widget=forms.Textarea)

class CreatePago(forms.Form):
    OPCIONES = (
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta'),
        ('PayPal', 'PayPal'),
        ('Criptomoneda', 'Criptomoneda'),
        ('Transferencia', 'Transferencia'),
    )

    seleccion = forms.ChoiceField(
        choices=OPCIONES, 
        widget=forms.RadioSelect,
        label="Elige una opción"
    )

    