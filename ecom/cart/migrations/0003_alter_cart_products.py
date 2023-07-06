# Generated by Django 4.2.1 on 2023-06-06 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_product_image'),
        ('cart', '0002_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(through='cart.CartItem', to='user.product'),
        ),
    ]
