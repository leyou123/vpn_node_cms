# Generated by Django 2.1.4 on 2022-06-30 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0012_auto_20220630_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodeconfig',
            name='test_node',
            field=models.BooleanField(blank=True, default=0, null=True, verbose_name='测试节点'),
        ),
        migrations.AlterField(
            model_name='nodeconfig',
            name='run_status',
            field=models.IntegerField(choices=[(0, '停止'), (1, '正常运行'), (2, '正在启动服务'), (3, '检测可用'), (4, '已生成域名'), (5, '已生成证书'), (6, '正在关闭服务'), (7, '节点测试')], default=0, verbose_name='运行状态'),
        ),
    ]
