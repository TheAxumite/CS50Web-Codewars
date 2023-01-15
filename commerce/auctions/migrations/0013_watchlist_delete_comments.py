# Generated by Django 4.1.5 on 2023-01-12 18:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0012_alter_item_image_file"),
    ]

    operations = [
        migrations.CreateModel(
            name="WatchList",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="watcher",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "watchlist_item",
                    models.ManyToManyField(
                        blank=True, related_name="items", to="auctions.item"
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Comments",
        ),
    ]