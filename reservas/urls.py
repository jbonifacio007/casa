from django.urls import path
from .views import calendario,incluir_reserva

urlpatterns = [
    path(
        "calendario/",
        calendario,
        name="calendario"

    ),
    path(
        "incluir_reserva/",
        incluir_reserva,
        name="incluir_reserva"

    ),

]