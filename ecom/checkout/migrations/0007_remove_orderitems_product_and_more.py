# Generated by Django 4.2.1 on 2023-06-27 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0006_remove_order_to_address_order_city_order_country_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitems',
            name='product',
        ),
        migrations.RemoveField(
            model_name='orderitems',
            name='product_size',
        ),
        migrations.AddField(
            model_name='orderitems',
            name='product_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='orderitems',
            name='product_offer_price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitems',
            name='product_photo',
            field=models.ImageField(default=1, upload_to='images/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitems',
            name='product_price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitems',
            name='size',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
