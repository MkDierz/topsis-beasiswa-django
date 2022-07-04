from django.urls import path

from app.views import analysis, create, index

urlpatterns = [
    path("", index, name="index"),
    path("create/", create, name="create"),
    path("analyze/", analysis, name="analyze"),
]
