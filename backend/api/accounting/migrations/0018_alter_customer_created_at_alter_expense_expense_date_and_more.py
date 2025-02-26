# Generated by Django 5.1.4 on 2025-02-10 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0017_alter_customer_options_alter_expense_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='expense',
            name='expense_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='financialtransaction',
            name='transaction_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='purchase_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='sale',
            name='sale_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='upload',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
