# Generated by Django 4.1 on 2022-12-08 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0015_recipe_image_thousand_on_thousand"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="discount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
