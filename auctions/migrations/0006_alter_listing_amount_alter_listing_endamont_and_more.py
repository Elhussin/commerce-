# Generated by Django 5.0.1 on 2024-02-06 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_listing_amount_alter_listing_endamont_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='amount',
            field=models.FloatField(max_length=64),
        ),
        migrations.AlterField(
            model_name='listing',
            name='endAmont',
            field=models.FloatField(default=0, max_length=64),
        ),
        migrations.AlterField(
            model_name='paid',
            name='Paid_amount',
            field=models.FloatField(max_length=64),
        ),
    ]
