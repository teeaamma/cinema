# Generated by Django 3.2.16 on 2024-11-29 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Ожидает'), ('CONFIRMED', 'Подтверждено'), ('CANCELLED', 'Отменено')], default='PENDING', max_length=10, verbose_name='Статус'),
        ),
    ]
