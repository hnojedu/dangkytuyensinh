# Generated by Django 4.2 on 2023-05-08 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tuyensinh', '0007_application_anh_3x4'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='ma_ho_so',
            field=models.CharField(null=True),
        ),
    ]
