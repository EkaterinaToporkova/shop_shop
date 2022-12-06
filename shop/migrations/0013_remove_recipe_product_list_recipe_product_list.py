# Generated by Django 4.1 on 2022-12-06 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0012_alter_recipe_product_list"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recipe",
            name="product_list",
        ),
        migrations.AddField(
            model_name="recipe",
            name="product_list",
            field=models.ManyToManyField(to="shop.product"),
        ),
    ]
