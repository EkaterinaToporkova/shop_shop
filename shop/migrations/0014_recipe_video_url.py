# Generated by Django 4.1 on 2022-12-07 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0013_remove_recipe_product_list_recipe_product_list"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="video_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]