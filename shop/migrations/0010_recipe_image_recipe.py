# Generated by Django 4.1 on 2022-12-02 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0009_recipe"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="image_recipe",
            field=models.ImageField(default=None, upload_to="image_recipe"),
            preserve_default=False,
        ),
    ]