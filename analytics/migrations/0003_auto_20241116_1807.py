# Generated by Django 3.2.25 on 2024-11-16 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0005_remove_product_image_url"),
        ("analytics", "0002_auto_20241116_1802"),
    ]

    operations = [
        migrations.AddField(
            model_name="salesdata",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="salesdata",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="sales",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="salesdata",
            name="added_to_cart",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="salesdata",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sales_data",
                to="products.product",
            ),
        ),
        migrations.AlterField(
            model_name="salesdata",
            name="purchases",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="salesdata",
            name="views",
            field=models.IntegerField(default=0),
        ),
    ]
