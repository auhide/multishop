from django.urls import path
from . import views



app_name = "shops"

urlpatterns = [
    path("emag/", views.EmagView.as_view(), name="emag"),
    path("olx/", views.OlxView.as_view(), name="olx"),
    path("bazar/", views.BazarView.as_view(), name="bazar"),
    path("results/", views.ResultsView.as_view(), name="results")
]