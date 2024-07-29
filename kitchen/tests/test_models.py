from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from kitchen.models import DishType, Dish


class ModelsTestCase(TestCase):
    def test_dish_type_str(self):
        dish_type = DishType.objects.create(
            name="test_name"
        )
        self.assertEqual(
            str(dish_type), f"{dish_type.name}"
        )

    def test_cook_str(self):
        cook = get_user_model().objects.create(
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
        )
        self.assertEqual(
            str(cook),
            f"{cook.username} ({cook.first_name} {cook.last_name})"
        )

    def test_cook_years_of_experience(self):
        years_of_experience = 1
        password = "<PASSWORD>"
        username = "test_username"
        cook = get_user_model().objects.create_user(
            username="test_username",
            password=password,
            years_of_experience=years_of_experience,
        )
        self.assertEqual(cook.years_of_experience, years_of_experience)
        self.assertTrue(cook.check_password(password))
        self.assertEqual(cook.username, username)

    def dish(self):
        dish_type = DishType.objects.create(
            name="test_name"
        )
        dish = Dish.objects.create(
            name="test_name",
            dish_type=dish_type,
        )
        self.assertEqual(str(dish), dish.name)
