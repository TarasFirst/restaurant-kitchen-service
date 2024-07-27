from django.urls import path

from kitchen.views import (
    index,
    # CarListView,
    # CarDetailView,
    # CarCreateView,
    # CarUpdateView,
    # CarDeleteView,
    # DriverListView,
    # DriverDetailView,
    # DriverCreateView,
    # DriverLicenseUpdateView,
    # DriverDeleteView,
    # ManufacturerListView,
    # ManufacturerCreateView,
    # ManufacturerUpdateView,
    # ManufacturerDeleteView,
    # toggle_assign_to_car,
)

urlpatterns = [
    path("", index, name="index"),
]

app_name = "kitchen"
