# Generated by Django 5.0.1 on 2024-02-08 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='paid',
            name='add_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.CharField(max_length=64),
        ),
    ]