# Generated by Django 4.1.4 on 2022-12-14 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_c_tier_customer_ctier'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='PDiscountRate',
            field=models.IntegerField(null=True),
        ),
    ]
