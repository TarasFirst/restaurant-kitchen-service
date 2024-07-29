from django.test import TestCase, override_settings

from kitchen.forms import CookCreationForm


class FormTests(TestCase):
    @override_settings(AUTH_PASSWORD_VALIDATORS=[])
    def test_cook_creation_form_with_valid_license_number(self):
        form_data = {
            "username": "new_user",
            "password1": "Password1",
            "password2": "Password1",
            "first_name": "new_first_name",
            "last_name": "new_last_name",
            "years_of_experience": 1,
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form.data)
