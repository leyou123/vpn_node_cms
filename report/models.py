from django.db import models

# Create your models here.

class NodeBlack(models.Model):

    """
        节点黑名单
    """

    node_ip = models.CharField(u"节点ip", max_length=128, blank=True, null=True, db_index=True)
    node_name = models.CharField(u"节点名称", max_length=128, blank=True, null=True, db_index=True)
    ping_rate = models.FloatField(u"ping成功率", default=0, db_index=True)
    connect_rate = models.FloatField(u"连接成功率", default=0, db_index=True)
    country = models.CharField(u"国家", max_length=128, blank=True, null=True, db_index=True)


    class Meta:
        verbose_name = '节点黑名单'
        verbose_name_plural = verbose_name