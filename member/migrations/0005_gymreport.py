# Generated by Django 4.2.3 on 2023-08-05 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_alter_members_fee_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='GymReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('revenue', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
