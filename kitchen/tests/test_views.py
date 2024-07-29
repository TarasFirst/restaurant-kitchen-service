import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, override_settings
from django.urls import reverse

from kitchen.models import DishType, Cook, Dish

DISH_TYPE_URL = reverse("kitchen:dish-type-list")


class PublicDishTypeTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(DISH_TYPE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDishTypeTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_dish_type(self):
        DishType.objects.create(name="test_dish_type")
        response = self.client.get(DISH_TYPE_URL)
        self.assertEqual(response.status_code, 200)
        dish_type_all = DishType.objects.all()
        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(dish_type_all),
        )
        self.assertTemplateUsed(response, "kitchen/dish_type_list.html")


class PrivateCookTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    @override_settings(AUTH_PASSWORD_VALIDATORS=[])
    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "Password1",
            "password2": "Password1",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
            "years_of_experience": 10,
        }
        self.client.post(reverse("kitchen:cook-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, "new_first_name")
        self.assertEqual(new_user.last_name, "new_last_name")
        self.assertEqual(new_user.years_of_experience, 10)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "search_term,expected_results",
    [
        pytest.param(
            "testcook",
            ["testcook1",
             "testcook2"],
            id="partial_match"
        ),
        pytest.param(
            "",
            ["testcook1", "testcook2", "cook3"],
            id="empty_search"
        ),
        pytest.param("nonexistent", [], id="no_results"),
    ],
)
def test_cook_search(client, search_term, expected_results):
    user = get_user_model().objects.create_user(
        username="testuser", password="testpass"
    )
    client.force_login(user)

    Cook.objects.create(
        username="cook1",
        password="testpass",
        years_of_experience=5
    )
    Cook.objects.create(
        username="cook2",
        password="testpass",
        years_of_experience=0
    )
    Cook.objects.create(
        username="cook3",
        password="testpass",
        years_of_experience=1
    )

    response = client.get(
        reverse("kitchen:cook-list"),
        {"username": search_term}
    )
    assert response.status_code == 200

    response_content = response.content.decode()
    for cook_username in expected_results:
        assert cook_username in response_content
    for cook in Cook.objects.exclude(username__in=expected_results):
        assert cook.username not in response_content


@pytest.mark.django_db
@pytest.mark.parametrize(
    "search_term,expected_results",
    [
        pytest.param("Dish_X", ["Dish_X1", "Dish_X2"], id="partial_match"),
        pytest.param(
            "",
            ["Dish_X1", "Dish_X2", "Dish_Y1"],
            id="empty_search"),
        pytest.param("nonexistent", [], id="no_results"),
    ],
)
def test_dish_search(client, search_term, expected_results):
    user = get_user_model().objects.create_user(
        username="testuser", password="testpass"
    )
    client.force_login(user)

    dish_type = DishType.objects.create(name="TestDishType")

    Dish.objects.create(model="Dish_X1", dish_type=dish_type)
    Dish.objects.create(model="Dish_X2", dish_type=dish_type)
    Dish.objects.create(model="DishY1", dish_type=dish_type)

    response = client.get(reverse("kitchen:dish-list"), {"name": search_term})
    assert response.status_code == 200

    response_content = response.content.decode()
    for dish_name in expected_results:
        assert dish_name in response_content
    for dish in Dish.objects.exclude(name__in=expected_results):
        assert dish.name not in response_content


@pytest.mark.django_db
@pytest.mark.parametrize(
    "search_term,expected_results",
    [
        pytest.param(
            "TestDishType",
            ["TestDishType1", "TestDishType2"],
            id="partial_match",
        ),
        pytest.param(
            "",
            ["TestDishType1", "TestDishType2", "OtherDishType"],
            id="empty_search",
        ),
        pytest.param("nonexistent", [], id="no_results"),
    ],
)
def test_dish_type_search(client, search_term, expected_results):
    user = get_user_model().objects.create_user(
        username="testuser", password="testpass"
    )
    client.force_login(user)

    DishType.objects.create(name="TestDishTyper1")
    DishType.objects.create(name="TestDishType2")
    DishType.objects.create(name="OtherDishType")

    response = client.get(
        reverse("kitchen:dish-type-list"),
        {"name": search_term}
    )
    assert response.status_code == 200

    response_content = response.content.decode()
    for dish_type_name in expected_results:
        assert dish_type_name in response_content
    for dish_type in DishType.objects.exclude(
            name__in=expected_results
    ):
        assert dish_type.name not in response_content


class CookIntegrationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="adminuser", password="adminpass123"
        )
        self.client.force_login(self.user)

    @override_settings(AUTH_PASSWORD_VALIDATORS=[])
    def test_create_cook_and_check_in_list(self):
        form_data = {
            "username": "new_cook",
            "password1": "A1b2C3d4E5",
            "password2": "A1b2C3d4E5",
            "first_name": "New",
            "last_name": "New_test",
            "years_of_experience": 2,
        }

        create_response = self.client.post(
            reverse("kitchen:cook-create"), data=form_data
        )

        if create_response.status_code != 302:
            print(create_response.context["form"].errors)
        self.assertEqual(create_response.status_code, 302)

        new_cook = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertIsNotNone(new_cook)
        self.assertEqual(new_cook.first_name, form_data["first_name"])
        self.assertEqual(new_cook.last_name, form_data["last_name"])
        self.assertEqual(
            new_cook.years_of_experience,
            form_data["years_of_experience"]
        )

        list_response = self.client.get(reverse("kitchen:cook-list"))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, new_cook.username)
