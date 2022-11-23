# Generated by Django 4.1 on 2022-11-16 13:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0005_alter_product_image_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="image_url",
            field=models.ImageField(
                default=django.utils.timezone.now, upload_to="img_product"
            ),
            preserve_default=False,
        ),
    ]