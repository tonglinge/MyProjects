# from django.test import TestCase

# Create your tests here.

from afcat.cmdb import models
from django.db import connections


def auto_update_ids(custid=None):
    """
    初始化ids表,默认客户编号是1001
    :return:
    """
    if not custid:
        custid = 1001
    startid = int("{0}{1}".format(custid, 1))
    cursor = connections["cmdb"].cursor()
    # 初始化表
    cursor.execute("SELECT app_label, model FROM django_content_type "
                   "WHERE app_label in('account','cmdb') "
                   "and model not in ('account')")
    for rec in cursor.fetchall():
        app_label, model = rec
        models.IDS.objects.create(tablename="{0}_{1}".format(app_label, model), nextid=startid)

    records = models.IDS.objects.all()
    for rec in records:
        tablename = rec.tablename
        sql = "select max(id) lastid from {0}".format(tablename)
        print(sql)
        cursor.execute(sql)
        lastid = cursor.fetchall()[0][0]
        if not lastid or lastid < 10010:
            lastid = 10010
        print("lastid", lastid)
        custcode = str(lastid)[:4]
        record_id = str(lastid)[4:]
        print("custcode, record_id", custcode, record_id)
        new_id = int("{0}{1}".format(custcode, int(record_id) + 1))
        rec.nextid = new_id
        rec.save()


