# Generated by Django 3.1.7 on 2023-04-10 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localpay', '0012_auto_20230410_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_mon',
            name='comment',
            field=models.TextField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
