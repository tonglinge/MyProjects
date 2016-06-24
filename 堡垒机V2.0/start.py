#!/usr/bin/env python
from conf import settings
from bin import initdb, main
from template import templates

if __name__ == "__main__":
    # 初始化数据库
    initdb.init_run()
    # 获取模板文件
    show_menu = templates.TITLE
    print(show_menu)
    main.run()
