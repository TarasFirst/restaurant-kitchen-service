from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import models

from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "dish_type"
        verbose_name_plural = "dish_types"

    def __str__(self):
        return self.name


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.pk})

    def delete(self, *args, **kwargs):
        if self.is_superuser:
            raise PermissionDenied("You cannot delete a superuser.")
        super(Cook, self).delete(*args, **kwargs)


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    cooks = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="dishes"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "dish"
        verbose_name_plural = "dishes"

    def __str__(self):
        return f"{self.name} ({self.dish_type})"
