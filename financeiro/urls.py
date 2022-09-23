from django.urls import path
from .views import gerarparcela,gerardespesaparcela,consultapagmes,consulta

urlpatterns = [

    path(
        "gerarparcela/<int:parcelamento_id>/",
        gerarparcela,
        name="gerarparcela"

    ),
    path(
        "gerardespesaparcela/<int:despesa_id>/",
        gerardespesaparcela,
        name="gerardespesaparcela"

    ),

    path(
        "consultapagmes/",
        consultapagmes,
        name="consultapagmes"

    ),
    path('consulta/', consulta),

]