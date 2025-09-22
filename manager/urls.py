from django.urls import path

from manager.views import index, PositionListView

urlpatterns = [
    path("", index, name="index"),
    path("positions/", PositionListView.as_view(), name="position-list"),
]


app_name = "manager"