# Generated by Django 3.1.6 on 2021-04-29 08:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('konekt', '0006_uploadcv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='job',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='link_cv',
            field=models.FileField(blank=True, default='', upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'odf', 'odt'])]),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='name',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='status',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.DeleteModel(
            name='UploadCV',
        ),
    ]
