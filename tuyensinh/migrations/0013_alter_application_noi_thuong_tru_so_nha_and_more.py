# Generated by Django 4.2 on 2023-05-14 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tuyensinh', '0012_application_generated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='noi_thuong_tru_so_nha',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='noi_thuong_tru_to',
            field=models.CharField(max_length=255, null=True),
        ),
    ]