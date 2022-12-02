# Generated by Django 4.1 on 2022-12-02 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0008_product_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="Recipe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="recipe_name")),
                (
                    "description",
                    models.CharField(max_length=1000, verbose_name="description"),
                ),
                (
                    "product_list",
                    models.CharField(max_length=1000, verbose_name="product_list"),
                ),
                ("recipe_note", models.TextField(blank=True, null=True)),
            ],
            options={
                "ordering": ["pk"],
            },
        ),
    ]
