# Generated by Django 3.1.7 on 2023-04-10 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localpay', '0008_auto_20230410_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_mon',
            name='refill',
            field=models.BigIntegerField(default=0, null=True, verbose_name='Пополнение баланса'),
        ),
        migrations.AddField(
            model_name='user_mon',
            name='write_off',
            field=models.BigIntegerField(default=0, null=True, verbose_name='Списание баланса'),
        ),
    ]