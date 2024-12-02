# Generated by Django 3.2.25 on 2024-11-05 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=254)),
                (
                    "friendly_name",
                    models.CharField(blank=True, max_length=254, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
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
                (
                    "sku",
                    models.CharField(blank=True, max_length=254, null=True),
                ),
                ("name", models.CharField(max_length=254)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    "discount_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=6, null=True
                    ),
                ),
                (
                    "rating",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=6, null=True
                    ),
                ),
                ("stock_quantity", models.IntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "size",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "image_url",
                    models.URLField(blank=True, max_length=1024, null=True),
                ),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to=""),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="products.category",
                    ),
                ),
            ],
        ),
    ]
