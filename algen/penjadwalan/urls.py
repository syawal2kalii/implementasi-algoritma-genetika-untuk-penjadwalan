from django.conf.urls import url
from . import views

urlpatterns = [
    url("generate/", views.generate, name="generate"),
    url("tes/", views.tes, name="tes"),
]
