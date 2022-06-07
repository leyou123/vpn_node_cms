from django.db import models
from node_manage.settings import URL
from django.core.exceptions import ValidationError
import time
import datetime


class Country(models.Model):
    """
        国家
    """
    id = models.AutoField(primary_key=True, auto_created=True)
    acronym = models.CharField(u"国家缩写", max_length=128, db_index=True, unique=True)
    name = models.CharField(u"中文国家", max_length=128, db_index=True, unique=True)
    english_name = models.CharField(u"英语国家",default="", max_length=128, db_index=True)
    national_flag = models.CharField(u"国旗", max_length=255, null=True, default=None, blank=True)

    class Meta:
        verbose_name = '国家'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Operator(models.Model):
    """
        运营商
    """
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(u"名称", max_length=128, db_index=True, unique=True)
    snapshot = models.CharField(u"镜像", max_length=128, db_index=True, unique=True)

    class Meta:
        verbose_name = '运营商'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class InstanceConfig(models.Model):
    """
        实例配置
    """
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(u"名称", max_length=128, db_index=True, unique=True)
    operator = models.ForeignKey(Operator, on_delete=models.SET_NULL, verbose_name='运营商', blank=True, null=True)
    config = models.CharField(u"实例配置", max_length=128, null=True, default=None, blank=True)

    class Meta:
        verbose_name = '实例配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = f"{self.operator.name}_{self.name}"

        return name


class Region(models.Model):
    """
        服务器地区
    """
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(u"名称", max_length=128, db_index=True, unique=True)
    english_name = models.CharField(u"英语地区", default="",max_length=128, db_index=True)
    operator = models.ForeignKey(Operator, on_delete=models.SET_NULL, verbose_name='运营商', blank=True, null=True)
    region = models.CharField(u"地区", max_length=128, null=True, default=None, blank=True)

    class Meta:
        verbose_name = '地区'
        verbose_name_plural = verbose_name

    def __str__(self):
        name = f"{self.operator.name}_{self.name}"
        return name


class NodeConfig(models.Model):
    """
        节点配置
    """

    RUN_STATUS = (
        (0, "停止"),
        (1, "正常运行"),
        (2, "正在启动服务"),
        (3, "检测可用"),
        (4, "已生成域名"),
        (5, "已生成证书"),
        (6, "正在关闭服务"),

    )

    STATUS = (
        (0, "不可用"),
        (1, "可用"),
        (2, "未开启"),
    )

    TROJAN_TYPE = (
        (1, "免费线路"),
        (2, "VIP线路"),
    )

    id = models.AutoField(primary_key=True, auto_created=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, verbose_name='国家', blank=True, null=True)
    operator = models.ForeignKey(Operator, on_delete=models.SET_NULL, verbose_name='运营商', blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, verbose_name='服务器地区', blank=True, null=True)
    old_instance_id = models.CharField(u"等待删除实例ID", max_length=128, null=True, default=None, blank=True)
    instance_id = models.CharField(u"实例ID", max_length=128, null=True, default=None, blank=True)
    domain_id = models.CharField(u"域名ID", max_length=128, null=True, default=None, blank=True)
    ssl_id = models.CharField(u"证书ID", max_length=128, null=True, default=None, blank=True)
    node_type = models.IntegerField(u"节点类型", default=1, choices=TROJAN_TYPE)
    domain = models.CharField(u"域名", max_length=128, null=True, default=None, blank=True)
    name = models.CharField(u"名称", max_length=128, db_index=True, unique=True)
    ip = models.CharField(u"ip", max_length=128, null=True, default=None, blank=True)
    config = models.ForeignKey(InstanceConfig, on_delete=models.SET_NULL, verbose_name='实例配置', blank=True, null=True)
    cname_validation_p1 = models.CharField(u"cname_p1", max_length=255, null=True, default=None, blank=True)
    cname_validation_p2 = models.CharField(u"cname_p2", max_length=255, null=True, default=None, blank=True)
    status = models.IntegerField(u"连接状态", default=2, choices=STATUS)
    info = models.CharField(u"信息", max_length=255, null=True, default=None, blank=True)
    run_status = models.IntegerField(u"运行状态", default=0, choices=RUN_STATUS)
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = '节点配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def to_json(self):
        instance_id = ""
        config = ""
        ip = ""
        domain = ""
        old_instance_id = ""
        if self.instance_id:
            instance_id = self.instance_id

        if self.old_instance_id:
            old_instance_id = self.old_instance_id
        if self.domain:
            domain = self.domain
        if self.ip:
            ip = self.ip
        if self.config:
            config = self.config.config

        obj = {
            "id": self.id,
            "country": self.country.english_name,
            "snapshot": self.operator.snapshot,
            "operator": self.operator.name,
            "instance_id": instance_id,
            "old_instance_id":old_instance_id,
            "region": self.region.english_name,
            "region_id": self.region.region,
            "domain": domain,
            "name": self.name,
            "ip": ip,
            "node_type":self.node_type,
            "config": config,
            "status": self.status,
            "run_status": self.run_status,
            "national_flag": self.country.national_flag,
            "cert_id":self.ssl_id,
            "cname_validation_p1":self.cname_validation_p1,
            "cname_validation_p2": self.cname_validation_p2

        }
        return obj


class TrajonNode(models.Model):
    """
    节点
    """

    TROJAN_TYPE = (
        (1, "免费线路"),
        (2, "VIP线路"),
    )

    QUICK_TYPE = (
        (0, "正常"),
        (1, "快速"),
    )

    id = models.AutoField(primary_key=True, auto_created=True)
    instance_id = models.CharField(u"实例ID", max_length=64, null=True, default=None, blank=True)
    name = models.CharField(u"节点名字", max_length=128, null=True, default=None, blank=True)
    host = models.CharField(u"域名", max_length=128, null=True, default=None, blank=True)
    ip = models.CharField(u"ip", max_length=128, null=True, default=None, blank=True)
    port = models.CharField(u"端口", max_length=128, null=True, default=None, blank=True)
    node_type = models.IntegerField(u"节点类型", default=1, choices=TROJAN_TYPE)
    country = models.CharField(u"国家", max_length=128, null=True, default=None, blank=True)
    region = models.CharField(u"地区", max_length=64, null=True, default=None, blank=True)
    cpu = models.CharField(u"cpu使用率", max_length=64, null=True, default=None, blank=True)
    memory = models.CharField(u"内存使用率", max_length=64, null=True, default=None, blank=True)
    network_send = models.CharField(u"发送流量带宽(单位:MB)", max_length=64, null=True, default=None, blank=True)
    network_recv = models.CharField(u"接受流量带宽(单位:MB)", max_length=64, null=True, default=None, blank=True)
    already_flow = models.CharField(u"已使用流量(单位:GB)", max_length=64, null=True, default=None, blank=True)

    download = models.CharField(u"上传测速(单位:MB)", max_length=64, default="", blank=True)
    upload = models.CharField(u"上传测速(单位:MB)", max_length=64, default="", blank=True)
    ping = models.CharField(u"ping值(单位:ms)", max_length=64, default="", blank=True)
    total_flow = models.CharField(u"总流量(单位:GB)", max_length=64, null=True, default=None, blank=True)
    speed_limit = models.FloatField(u"节点限速(单位:MB)", default=0)

    circle_image_url = models.CharField(u"圆形国旗", max_length=255, null=True, default=None, blank=True)
    # #
    image_url = models.CharField(u"方形国旗", max_length=255, null=True, default=None, blank=True)

    connected = models.IntegerField(u"连接人数", default=0)
    max_user_connected = models.IntegerField(u"最大连接人数", default=0)
    cnt = models.IntegerField(u"强力推荐值", default=0)
    tag = models.CharField(u"标签", max_length=255, null=True, default=None, blank=True)
    quick_access = models.IntegerField(u"快捷访问", default=0, choices=QUICK_TYPE)

    description = models.CharField(u"节点描述", max_length=255, null=True, default=None, blank=True)
    status = models.BooleanField(u"状态", default=0)
    white = models.TextField(u"白名单", default="", blank=True)
    black = models.TextField(u"黑名单", default="", blank=True)
    test_url = models.CharField(u"测试网址", max_length=255, null=True, default="", blank=True)
    connect_data = models.TextField(u"连接数据", default="", blank=True)

    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def conv_update_date(self):
        if self.update_time:
            this_date = str(self.update_time.strftime('%Y-%m-%d %H:%M:%S'))
            str_date = datetime.datetime.strptime(this_date, '%Y-%m-%d %H:%M:%S')
            # 把datetime转变为时间戳
            this_date = int(time.mktime(str_date.timetuple()))
            return this_date
        else:
            return 0

    def __calculate_recommended_value(self):
        try:
            cpu = round(float(self.cpu.replace("%", "")) / 100, 2)
            mem = round(float(self.memory.replace("%", "")) / 100, 2)

            already_flow = float(self.already_flow)
            total_flow = float(self.total_flow)
            flow = round(already_flow / total_flow, 2)
            if flow >= 0.95:
                print("流量")
                return -40

            download = 0
            if self.download:
                download = float(self.download)

            upload = 0
            if self.upload:
                upload = float(self.upload)

            user = self.connected
            # print(f"ip:{self.ip},cpu:{cpu},mem:{mem},flow:{flow}")
            recommended_value = (2 - cpu * 1.3 - mem * 1.3 - 0.5 * flow) * 80 + self.cnt
	    # recommended_value = (2 - cpu * 1.3 - mem * 1.3 - 0.5 * flow) * 80 + self.cnt - self.connected
            # recommended_value = (1 - cpu) * 10 + (1 - mem) * 10 + (1 - flow) * 10 + (
            #             1 - user / self.max_user_connected) * 50 + self.cnt

            # recommended_value = download*0.5+upload*0.3+int((1 - cpu) * 20 + (1 - mem) * 20 + (1 - bandwidth) * 10 +(1 - user / self.max_user_connected) * 50) + self.cnt
            return int(recommended_value)
        except Exception as e:
            print(e)
            return 0

    def use_flow_rate(self):
        use_flow_rate = 0
        if self.already_flow and self.total_flow:
            already_flow = float(self.already_flow)
            total_flow = float(self.total_flow)
            use_flow_rate = already_flow / total_flow

        return use_flow_rate

    def to_dict(self):

        imgUrl = ""
        circle_image_url = ""
        description = ""
        tag = ""
        black = ""

        if self.image_url:
            imgUrl = f"https://www.9527.click/static/images/country/orthogon/{self.image_url}.png"

        if self.circle_image_url:
            circle_image_url = f"https://www.9527.click/static/images/country/circle/{self.circle_image_url}.png"

        if self.description:
            description = self.description

        if self.tag:
            tag = self.tag

        if self.black:
            black = self.black

        test_url = ""
        if self.test_url:
            test_url = self.test_url

        obj = {
            "id": self.id,
            "name": self.name,
            "instance_id": self.instance_id,
            "host": self.host,
            "cpu": self.cpu,
            "ip": self.ip,
            "port": self.port,
            "node_type": self.node_type,
            "country": self.country,
            "region": self.region,
            "memory": self.memory,
            "network_send": self.network_send,
            "network_recv": self.network_recv,
            "already_flow": self.already_flow,
            "download": self.download,
            "upload": self.upload,
            "ping": self.ping,
            "total_flow": self.total_flow,
            "image_url": imgUrl,
            "circle_image_url": circle_image_url,
            "status": self.status,
            "weights": self.__calculate_recommended_value(),
            "connected": self.connected,
            "max_user_connected": self.max_user_connected,
            "cnt": self.cnt,
            "description": description,
            "quick_access": self.quick_access,
            "tag": tag,
            "black": black,
            "test_url": test_url,
            "white": self.white,
            "connect_data": self.connect_data,
            "update_time": self.conv_update_date()
        }
        return obj

    def save(self, *args, **kwargs):

        if self.black:
            if "," not in self.black:
                raise ValidationError('黑名单,请用,隔开')

        if self.white:
            if "," not in self.white:
                raise ValidationError('白名单,请用,隔开')

        if self.white and self.black:
            #
            while_list = self.white.split(',')
            black_list = self.black.split(',')

            while_list = [i for i in while_list if i != '']
            black_list = [j for j in black_list if j != '']

            res = list(set(while_list).intersection(set(black_list)))

            if res:
                msg = "".join(res)
                raise ValidationError(f"黑白名单冲突:{msg}")

        super().save(*args, **kwargs)
