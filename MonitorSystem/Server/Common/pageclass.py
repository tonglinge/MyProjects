# coding:utf-8
from Server.settings import DB_PAGE_PER_COUNT

PAGE_PER_NUM = DB_PAGE_PER_COUNT


class PageInfo(object):
    def __init__(self, recordcount, pageindex=1):
        self.Pagenum = pageindex
        self.RecCount = recordcount
        self.PerCount = PAGE_PER_NUM
        self.PageLast = 1
        self.PageNext = pageindex + 1
        self.TotalPage = 0

    def Count(self):
        # 获取总页数
        if self.RecCount % self.PerCount > 0:
            self.TotalPage = self.RecCount / self.PerCount + 1
        else:
            self.TotalPage = self.RecCount / self.PerCount

        # 获取上一页页码
        if self.Pagenum > 1:
            self.PageLast = self.Pagenum - 1
        else:
            self.PageLast = 1

        # 获取下一页页码
        if self.Pagenum >= self.TotalPage:
            self.PageNext = self.TotalPage
        else:
            self.PageNext = self.Pagenum + 1
