# Generated by Django 4.2.3 on 2023-08-05 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_alter_members_fee_date_alter_payment_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='members',
            name='fee_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
