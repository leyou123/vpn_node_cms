# Generated by Django 2.1.4 on 2022-06-30 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0010_remove_trajonnode_hide_switch'),
    ]

    operations = [
        migrations.AddField(
            model_name='trajonnode',
            name='script_status',
            field=models.BooleanField(default=0, verbose_name='θζ¬ηΆζ'),
        ),
    ]
