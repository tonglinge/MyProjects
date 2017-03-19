#! /usr/bin/env python
# encoding: utf8

from xlsxwriter import Workbook


class ExportExcel(Workbook):
    constant_memory = True  # 固定占用内存空间，用于大文件存储，
    tmpdir = None  # 用于临时存储文件的目录，如果启用，则必须先创建该目录，否则不能正常工作
    in_memory = True  # 该选项优先于constant_memory，不使用临时文件
    strings_to_numbers = True  # 启用字符串存储为数字，避免
    strings_to_formulas = True  # 启用字符串公式，默认true
    strings_to_urls = True  # 启用urls，默认true
    nan_inf_to_errors = False  # 处理NAN/INF
    default_date_format = "dd/mm/yy"
    # Font
    font_name = None  # 字体类型excel出现警告
    font_size = None  # 字体大小
    font_color = None  # 字体颜色
    bold = None  # 字体加粗
    italic = None  # 斜体
    underline = None  # 添加下划线
    font_strikeout = None  # 字体是否带删除线
    font_script = None
    # Number
    num_format = None  # 数值格式化
    # Protection
    locked = None  # 是否锁定
    hidden = None  # 是否隐藏
    # Alignment
    align = None  # 水平对齐
    valign = None  # 垂直对齐
    rotation = None  # 旋转
    text_wrap = None  # 文本换行
    text_justlast = None  # 最后一行向右对齐
    center_across = None
    indent = None  # 缩进
    shrink = None
    # Pattern
    pattern = None
    bg_color = None  # 背景颜色
    fg_color = None  # 前景颜色
    # Border
    border = None  # 边框
    bottom = None  # 下边框
    top = None  # 上边框
    left = None  # 左边框
    right = None  # 左边框
    border_color = None  # 边框颜色
    bottom_color = None  # 下边框颜色
    top_color = None  # 上边框颜色
    left_color = None  # 左边框颜色
    right_color = None  # 右边框颜色

    def __init__(self, filename=None, options={}):
        super(ExportExcel, self).__init__(filename=filename, options=options)

    def write_title(self, title_list):
        pass
