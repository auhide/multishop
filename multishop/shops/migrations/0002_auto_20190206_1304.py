# Generated by Django 2.1 on 2019-02-06 11:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopsearch',
            old_name='keywords',
            new_name='searched_product',
        ),
        migrations.AlterField(
            model_name='shopsearch',
            name='maximum_price',
            field=models.PositiveIntegerField(default='Maximum', validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='shopsearch',
            name='minimum_price',
            field=models.PositiveIntegerField(default='Minimum', validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]