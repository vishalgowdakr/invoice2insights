# Generated by Django 5.1.4 on 2024-12-19 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0006_alter_invoice_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_file',
            field=models.ImageField(upload_to='invoices/'),
        ),
    ]