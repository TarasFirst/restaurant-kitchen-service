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
    DishTypeListView,
    # ManufacturerCreateView,
    # ManufacturerUpdateView,
    # ManufacturerDeleteView,
    # toggle_assign_to_car,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "dish_types/",
        DishTypeListView.as_view(),
        name="dish-type-list",
    ),
]

app_name = "kitchen"
