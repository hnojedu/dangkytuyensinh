# Generated by Django 4.2 on 2023-05-12 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tuyensinh', '0011_remove_application_anh_3x4'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='generated',
            field=models.BooleanField(default=False),
        ),
    ]