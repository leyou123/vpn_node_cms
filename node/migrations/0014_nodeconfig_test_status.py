# Generated by Django 2.1.4 on 2022-06-30 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0013_auto_20220630_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodeconfig',
            name='test_status',
            field=models.BooleanField(blank=True, default=0, null=True, verbose_name='测试状态'),
        ),
    ]
