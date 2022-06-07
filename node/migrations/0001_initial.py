# Generated by Django 2.1.4 on 2022-03-23 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('acronym', models.CharField(db_index=True, max_length=128, unique=True, verbose_name='国家缩写')),
                ('name', models.CharField(db_index=True, max_length=128, unique=True, verbose_name='中文国家')),
                ('national_flag', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='国旗')),
            ],
            options={
                'verbose_name': '国家',
                'verbose_name_plural': '国家',
            },
        ),
        migrations.CreateModel(
            name='InstanceConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=128, unique=True, verbose_name='名称')),
                ('config', models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='实例配置')),
            ],
            options={
                'verbose_name': '实例配置',
                'verbose_name_plural': '实例配置',
            },
        ),
        migrations.CreateModel(
            name='NodeConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('instance_id', models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='实例ID')),
                ('node_type', models.IntegerField(choices=[(1, '免费线路'), (2, 'VIP线路')], default=1, verbose_name='节点类型')),
                ('domain', models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='域名')),
                ('name', models.CharField(db_index=True, max_length=128, unique=True, verbose_name='名称')),
                ('ip', models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='ip')),
                ('status', models.IntegerField(choices=[(0, '不可用'), (1, '正常'), (2, '未配置')], default=2, verbose_name='状态')),
                ('run_status', models.IntegerField(choices=[(0, '停止'), (1, '正常'), (2, '运行中'), (3, '未配置')], default=3, verbose_name='运行状态')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('config', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='node.InstanceConfig', verbose_name='实例配置')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='node.Country', verbose_name='国家')),
            ],
            options={
                'verbose_name': '节点配置',
                'verbose_name_plural': '节点配置',
            },
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=128, unique=True, verbose_name='名称')),
                ('snapshot', models.CharField(db_index=True, max_length=128, unique=True, verbose_name='镜像')),
            ],
            options={
                'verbose_name': '运营商',
                'verbose_name_plural': '运营商',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=128, unique=True, verbose_name='名称')),
                ('region', models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='地区')),
                ('operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='node.Operator', verbose_name='运营商')),
            ],
            options={
                'verbose_name': '地区',
                'verbose_name_plural': '地区',
            },
        ),
        migrations.CreateModel(
            name='TrajonNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('instance_id', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='实例ID')),
                ('name', models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='节点名字')),
                ('host', models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='域名')),
                ('ip', models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='ip')),
                ('port', models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='端口')),
                ('node_type', models.IntegerField(choices=[(1, '免费线路'), (2, 'VIP线路')], default=1, verbose_name='节点类型')),
                ('country', models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='国家')),
                ('region', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='地区')),
                ('cpu', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='cpu使用率')),
                ('memory', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='内存使用率')),
                ('network_send', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='发送流量带宽(单位:MB)')),
                ('network_recv', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='接受流量带宽(单位:MB)')),
                ('already_flow', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='已使用流量(单位:GB)')),
                ('download', models.CharField(blank=True, default='', max_length=64, verbose_name='上传测速(单位:MB)')),
                ('upload', models.CharField(blank=True, default='', max_length=64, verbose_name='上传测速(单位:MB)')),
                ('ping', models.CharField(blank=True, default='', max_length=64, verbose_name='ping值(单位:ms)')),
                ('total_flow', models.CharField(blank=True, default=None, max_length=64, null=True, verbose_name='总流量(单位:GB)')),
                ('speed_limit', models.FloatField(default=0, verbose_name='节点限速(单位:MB)')),
                ('circle_image_url', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='圆形国旗')),
                ('image_url', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='方形国旗')),
                ('connected', models.IntegerField(default=0, verbose_name='连接人数')),
                ('max_user_connected', models.IntegerField(default=0, verbose_name='最大连接人数')),
                ('cnt', models.IntegerField(default=0, verbose_name='强力推荐值')),
                ('tag', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='标签')),
                ('quick_access', models.IntegerField(choices=[(0, '正常'), (1, '快速')], default=0, verbose_name='快捷访问')),
                ('description', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='节点描述')),
                ('status', models.BooleanField(default=0, verbose_name='状态')),
                ('white', models.TextField(blank=True, default='', verbose_name='白名单')),
                ('black', models.TextField(blank=True, default='', verbose_name='黑名单')),
                ('test_url', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='测试网址')),
                ('connect_data', models.TextField(blank=True, default='', verbose_name='连接数据')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
        migrations.AddField(
            model_name='nodeconfig',
            name='operator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='node.Operator', verbose_name='运营商'),
        ),
        migrations.AddField(
            model_name='nodeconfig',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='node.Region', verbose_name='服务器地区'),
        ),
        migrations.AddField(
            model_name='instanceconfig',
            name='operator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='node.Operator', verbose_name='运营商'),
        ),
    ]