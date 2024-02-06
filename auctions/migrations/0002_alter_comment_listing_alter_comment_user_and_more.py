# Generated by Django 5.0.1 on 2024-02-06 12:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='Listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Listing', to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='status',
            field=models.CharField(default='open', max_length=64),
        ),
        migrations.AlterField(
            model_name='paid',
            name='Listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listID', to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='paid',
            name='user_bids',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UserId', to=settings.AUTH_USER_MODEL),
        ),
    ]