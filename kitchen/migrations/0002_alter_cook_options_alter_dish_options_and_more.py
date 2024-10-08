# Generated by Django 5.0.7 on 2024-07-27 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("kitchen", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cook",
            options={"ordering": ["username"]},
        ),
        migrations.AlterModelOptions(
            name="dish",
            options={
                "ordering": ["name"],
                "verbose_name": "dish",
                "verbose_name_plural": "dishes",
            },
        ),
        migrations.AlterModelOptions(
            name="dishtype",
            options={
                "ordering": ["name"],
                "verbose_name": "dish_type",
                "verbose_name_plural": "dish_types",
            },
        ),
    ]
