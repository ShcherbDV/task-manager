from django.urls import path

from manager.views import (
    index,
    PositionListView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/create/", PositionCreateView.as_view(), name="position-create"),
    path("positions/<int:pk>/update/", PositionUpdateView.as_view(), name="position-update"),
    path("positions/<int:pk>/delete/", PositionDeleteView.as_view(), name="position-delete"),
]


app_name = "manager"