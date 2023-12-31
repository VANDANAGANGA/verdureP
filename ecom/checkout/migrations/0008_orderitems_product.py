# Generated by Django 4.2.1 on 2023-06-28 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_product_is_deleted'),
        ('checkout', '0007_remove_orderitems_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.product'),
            preserve_default=False,
        ),
    ]
