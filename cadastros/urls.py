from django.urls import path
from .views import index,index2

urlpatterns = [
    path(
        "",
        index,
        name="index"

    ),

    path(
        "index2",
        index2,
        name="index2"

    ),

]