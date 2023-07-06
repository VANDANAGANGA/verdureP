# Generated by Django 4.2.1 on 2023-06-12 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_profileaddress_house_name'),
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitems',
            name='product_size',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.productsize'),
            preserve_default=False,
        ),
    ]
