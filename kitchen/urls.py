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
    DishTypeCreateView,
    DishTypeUpdateView,
    DishTypeDeleteView,
    # toggle_assign_to_car,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "dish_types/",
        DishTypeListView.as_view(),
        name="dish-type-list",
    ),
    path(
        "dish_types/create/",
        DishTypeCreateView.as_view(),
        name="dish-type-create",
    ),
    path(
        "dish_types/<int:pk>/update/",
        DishTypeUpdateView.as_view(),
        name="dish-type-update",
    ),
    path(
        "dish_types/<int:pk>/delete/",
        DishTypeDeleteView.as_view(),
        name="dish-type-delete",
    ),
]

app_name = "kitchen"
