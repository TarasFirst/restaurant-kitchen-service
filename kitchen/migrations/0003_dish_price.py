# Generated by Django 5.0.7 on 2024-08-09 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kitchen", "0002_alter_cook_options_alter_dish_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="dish",
            name="price",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
            preserve_default=False,
        ),
    ]
