# Generated by Django 2.1 on 2019-02-06 09:58

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('price', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ShopSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords', models.CharField(max_length=150)),
                ('minimum_price', models.DecimalField(decimal_places=2, max_digits=3, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('maximum_price', models.DecimalField(decimal_places=2, max_digits=3, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='shop_search',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.ShopSearch'),
        ),
    ]
