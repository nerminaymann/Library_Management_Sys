# Generated by Django 5.1.1 on 2024-10-07 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_remove_returntransaction_borrow_transaction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='return_date',
            field=models.DateTimeField(null=True),
        ),
    ]
