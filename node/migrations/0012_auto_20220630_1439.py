# Generated by Django 2.1.4 on 2022-06-30 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0011_trajonnode_script_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trajonnode',
            name='script_status',
            field=models.BooleanField(blank=True, default=0, null=True, verbose_name='脚本状态'),
        ),
    ]
