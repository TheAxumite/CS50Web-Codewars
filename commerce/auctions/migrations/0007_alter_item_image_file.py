# Generated by Django 4.1.5 on 2023-01-12 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0006_item_image_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="image_file",
            field=models.ImageField(blank=True, null=True, upload_to="media/items/"),
        ),
    ]