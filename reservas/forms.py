from django import forms

from reservas.models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = [
            "membro", "data_inicio", "data_final",
        ]

