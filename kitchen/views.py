from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseRedirect
from django.shortcuts import render
# from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from kitchen.models import Cook, Dish, DishType
# from taxi.forms import (
#     DriverCreationForm,
#     DriverLicenseUpdateForm,
#     CarForm,
#     CarSearchForm,
#     DriverSearchForm,
#     ManufacturerSearchForm,
# )


@login_required
def index(request):

    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        "num_visits": num_visits + 1,
    }

    return render(request, "kitchen/index.html", context=context)


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 5
