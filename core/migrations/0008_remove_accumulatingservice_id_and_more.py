# Generated by Django 4.1.4 on 2022-12-15 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_wholesalecompany_pbarcode_product_wcname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accumulatingservice',
            name='id',
        ),
        migrations.AlterField(
            model_name='accumulatingservice',
            name='PBarcode',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='core.product'),
        ),
    ]