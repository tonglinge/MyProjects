#!/usr/bin/env python
from datetime import datetime
from module.tables import Op_Logs
from module.common import write_log

class BLL_Op_Logs(object):

    def __init__(self, opuser, sqlhelper):
        self.opuser = opuser
        self.mysql = sqlhelper

    def save_log(self, opmsglist, optype):
        """
        将操作日志写入数据库
        :param opmsg:要写入的消息记录
        :param optype: 日志类型 login / exec_cmd
        """
        try:
            # 连接数据库
            self.mysql.connect()
            for msg in opmsglist:
                newrecord = Op_Logs(uid=self.opuser.id,
                                    optype=optype,
                                    opdate=datetime.now(),
                                    opmsg=msg)
                self.mysql.session.add(newrecord)
            self.mysql.session.commit()
            # 执行完关闭数据库
            self.mysql.close()
        except Exception as e:
            write_log("[bll.op_log.save_log] {0}".format(e))


    def last_login_date(self):
        """
        获取用户上一次登录的时间
        """
        try:
            self.mysql.connect()
            op_rec = self.mysql.session.query(Op_Logs).filter(Op_Logs.uid==self.opuser.id).order_by(Op_Logs.opdate.desc()).first()
            self.mysql.close()
            return op_rec.opdate
        except Exception as e:
            write_log("[bll.op_log.last_login_date] {0}".format(e))