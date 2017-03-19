#! /usr/bin/env python
# encoding: utf8
"""
@author zengchunyun
@date 2016/10/28
"""
"""
from django.db import models, connection


class HostsManager(models.Manager):

    def getclass(self, sql):
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


class Hosts(models.Model):
    host_id = models.IntegerField(verbose_name=u'主机ID')
    host_name = models.CharField(max_length=64, verbose_name=u'主机名')

    objects = HostsManager()

    def __str__(self):
        return "{__class__.__name__},(host_id={host_id} host_name={host_name})".format(
            __class__=self.___class__,
            **self.__dict__
        )

"""
# class GraphsManager()
import xlsxwriter
from datetime import datetime
import io
"""

# workbook = xlsxwriter.Workbook("hello.xlsx")
output = io.BytesIO()
workbook = xlsxwriter.Workbook(output)

worksheet = workbook.add_worksheet('my')

bold = workbook.add_format({'bold': 1})
money = workbook.add_format({'num_format': '$#,##0'})
date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})
worksheet.set_column(1, 1, 15)
expenses = (
    ['Rent', '2013-01-13', 1000],
    ['Gas', '2013-01-14', 100],
    ['Food', '2013-01-16', 300],
    ['Gym', '2013-01-20', 50],
)
row = 1
col = 0
worksheet.write('A1', 'Item', bold)
worksheet.write('B1', 'Date', bold)
worksheet.write('C1', 'Cost', bold)
for item, date_str, cost in (expenses):
    date = datetime.strptime('%s' % date_str, '%Y-%m-%d')
    worksheet.write_string(row, col, item)
    worksheet.write_datetime(row, col+1, date, date_format)
    worksheet.write_number(row, col+2, cost, money)
    row += 1
worksheet.write(row, 0, 'Total', bold)
worksheet.write(row, 1, '=SUM(C2:C5)', money)

workbook.close()
"""

"""
柱状图
workbook = xlsxwriter.Workbook('chart.xlsx')
worksheet = workbook.add_worksheet('chart')
chart = workbook.add_chart({'type': 'column'})

data = [
    [1, 2, 3, 4, 5],
    [2, 4, 6, 8, 10],
    [3, 6, 9, 12, 15],
]
worksheet.write_column('A1', data[0])
worksheet.write_column('B1', data[1])
worksheet.write_column('C1', data[2])

chart.add_series({'values': '=chart!$A$1:$A$5'})
chart.add_series({'values': '=chart!$B$1:$B$5'})
chart.add_series({'values': '=chart!$C$1:$C$5'})

worksheet.insert_chart('A7', chart)
workbook.close()
"""

"""

# 折线图
workbook = xlsxwriter.Workbook("chart_line.xlsx")
worksheet = workbook.add_worksheet()
data = [10,40,50,20,10,50]
worksheet.write_column('A1', data=data)
chart = workbook.add_chart({'type': 'line'})
chart.add_series({'values': '=Sheet1!$A$1:$A$6'})
worksheet.insert_chart('C1', chart)
workbook.close()

"""
"""

饼图
workbook = xlsxwriter.Workbook('chart_pie.xlsx')
worksheet = workbook.add_worksheet()
chart = workbook.add_chart({'type': 'pie'})
data = [
    ['Pass', 'Fail'],
    [90, 10],
]

worksheet.write_column('A1', data=data[0])
worksheet.write_column('B1', data=data[1])

chart.add_series({
    'categories': '=Sheet1!$A$1:$A$2',
    'values': '=Sheet1!$B$1:$B$2',
    'points': [
        {'fill': {'color': 'green'}},
        {'fill': {'color': 'red'}},
    ],
})

worksheet.insert_chart('C3', chart=chart)
workbook.close()
"""

"""
轴图
workbook = xlsxwriter.Workbook('chart_secondary_axis.xlsx')
worksheet = workbook.add_worksheet()
data = [
    [2,3,4,5,6,7],
    [10,40,50,20,10,50],
]
worksheet.write_column('A2', data=data[0])
worksheet.write_column('B2', data=data[1])
chart = workbook.add_chart({'type': 'line'})
chart.add_series({
    'values': '=Sheet1!$A$2:$A$7',
    'y2_axis': True,
})

chart.add_series({
    'values': '=Sheet1!$B$2:$B$7',
})
chart.set_legend({'position': 'none'})
chart.set_y_axis({'name': 'Primary Y axis'})
chart.set_y2_axis({'name': 'Secondary Y axis'})
worksheet.insert_chart('D2', chart)
workbook.close()
"""

"""
饼图2
workbook = xlsxwriter.Workbook('chart_pie2.xlsx')
worksheet = workbook.add_worksheet()
data = [
    ['Apple', 60],
    ['Cherry', 30],
    ['Pecan', 10],
]

worksheet.add_table('A1:B4', {'data': data,
                              'columns': [
                                  {
                                      'header': 'Types'
                                  },
                                  {
                                      'header': 'Number'
                                  },
                              ]}
                    )
chart = workbook.add_chart({'type': 'pie'})
chart.add_series({
    'name': '=Sheet1!$A$1',
    'categories': '=Sheet1!$A$2:$A$4',
    'values': '=Sheet1!$B$2:$B$4',
})
worksheet.insert_chart('D2', chart)
workbook.close()
"""
"""
# 文本按钮
workbook = xlsxwriter.Workbook('textbox.xlsx')
worksheet = workbook.add_worksheet()
text = 'Formatted textbox'
options = {
    'width': 256,
    'height': 100,
    'x_offset': 10,
    'y_offset': 10,
    'font': {'color':'red', 'size': 14},
    'align': {'vertical': 'middle', 'horizontal': 'center'},
    'gradient': {'colors': ['#DDEBCF', '#9CB86E','#156B13']},
}
worksheet.insert_textbox('B2', text=text, options=options)
workbook.close()
"""



"""
与pandas结合

import pandas as pd
df = pd.DataFrame({'Data': [10,20,30,20,15,30, 45]})
writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')
writer.save()
"""

"""

import pandas as pd
import io

df = pd.DataFrame({'Data': [10,20,30,20,15,30,45]})
output = io.BytesIO()
writer = pd.ExcelWriter(output, engine='xlsxwriter')
pd.DataFrame().to_excel(writer, sheet_name='Sheet1')
writer.save()
xlsx_data = output.getvalue()
print(xlsx_data)
"""

"""
超链接

workbook = xlsxwriter.Workbook('hyperlink.xlsx')
worksheet = workbook.add_worksheet('Hyperlinks')
worksheet.set_column('A:A', 30)
url_format = workbook.add_format({
    'font_color': 'blue',
    'underline': 1
})
red_format = workbook.add_format({
    'font_color': 'red',
    'bold': 1,
    'underline': 1,
    'font_size': 12,
})
string = 'Python home'
top = 'Get the lastest Python news here.'
worksheet.write_url('A1', 'http://www.python.org')
worksheet.write_url('A3', 'http://www.python.org', url_format, string=string)
worksheet.write_url('A5', 'http://www.python.org', url_format, string, tip=top)
worksheet.write_url('A7', 'http://www.python.org', red_format)
worksheet.write_url('A9', 'mailto:850808158@qq.com', url_format, 'Mail me')
worksheet.write_string('A11', 'http://www/python.org')
workbook.close()
"""

"""

workbook = xlsxwriter.Workbook('array_formula.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('B1', 500)
worksheet.write('B2', 10)
worksheet.write('B5', 1)
worksheet.write('B6', 2)
worksheet.write('B7', 3)
worksheet.write('C1', 300)
worksheet.write('C2', 15)
worksheet.write('C5', 20234)
worksheet.write('C6', 21003)
worksheet.write('C7', 10000)
worksheet.write_formula('A1', '{=SUM(B1:C1*B2:C2)}')
worksheet.write_array_formula('A2:A2','{=SUM(B1:C1*B2:C2)}')
worksheet.write_array_formula('A5:A7', '{=TREND(C5:C7,B5:B7)}')
workbook.close()
"""

"""
workbook = xlsxwriter.Workbook('autofilter.xlsx')
worksheet1 = workbook.add_worksheet()
worksheet2 = workbook.add_worksheet()
worksheet3 = workbook.add_worksheet()
worksheet4 = workbook.add_worksheet()
worksheet5 = workbook.add_worksheet()
worksheet6 = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
textfile = open('autofilter_data.txt')
headers = textfile.readline().strip('\n').split()
data = []
for line in textfile:
    row_data = line.strip('\n').split()
    for i, item in enumerate(row_data):
        try:
            row_data[i] = float(item)
        except ValueError:
            pass
    data.append(row_data)

for worksheet in workbook.worksheets():
    worksheet.set_column('A:D', 12)
    worksheet.set_row(0, 20, bold)
    worksheet.write_row('A1', headers)

worksheet1.autofilter('A1:D51')
row = 1
for row_data in data:
    worksheet1.write_row(row, 0, row_data)
    row += 1
worksheet2.autofilter(0, 0, 50, 3)
worksheet2.filter_column(0, 'Region == East')
row = 1
for row_data in data:
    region = row_data[0]
    if region == 'East':
        pass
    else:
        worksheet2.set_row(row, options={'hidden': True})
    worksheet2.write_row(row, 0, row_data)
    row += 1
worksheet3.autofilter('A1:D51')
worksheet3.filter_column('A', 'x == East or x == South')
row = 1
for row_data in data:
    region = row_data[0]
    if region == 'East' or region == 'South':
        pass
    else:
        worksheet3.set_row(row, options={'hidden': True})
    worksheet3.write_row(row, 0, row_data)
    row += 1
worksheet4.autofilter('A1:D51')
worksheet4.filter_column('A', 'x == East')
worksheet4.filter_column('C', 'x > 3000 and x < 8000')
row = 1
for row_data in data:
    region = row_data[0]
    volume = int(row_data[2])
    if region == 'East' and volume > 3000 and volume < 8000:
        pass
    else:
        worksheet4.set_row(row, options={'hidden': True})
    worksheet4.write_row(row, 0, row_data)
    row += 1
worksheet5.autofilter('A1:D51')
worksheet5.filter_column('A', 'x == Blanks')
data[5][0] = ''
row = 1
for row_data in data:
    region = row_data[0]
    if region == '':
        pass
    else:
        worksheet5.set_row(row, options={'hidden': True})
    worksheet5.write_row(row, 0, row_data)
    row += 1

worksheet6.autofilter('A1:D51')
worksheet6.filter_column('A', 'x == NonBlanks')
row = 1
for row_data in data:
    region = row_data[0]
    if region != '':
        pass
    else:
        worksheet6.set_row(row, options={'hidden': True})
    worksheet6.write_row(row, 0, row_data)
    row += 1
workbook.close()
"""






"""
表格

workbook = xlsxwriter.Workbook('tables.xlsx')
worksheet1 = workbook.add_worksheet()
worksheet2 = workbook.add_worksheet()
worksheet3 = workbook.add_worksheet()
worksheet4 = workbook.add_worksheet()
worksheet5 = workbook.add_worksheet()
worksheet6 = workbook.add_worksheet()
worksheet7 = workbook.add_worksheet()
worksheet8 = workbook.add_worksheet()
worksheet9 = workbook.add_worksheet()
worksheet10 = workbook.add_worksheet()
worksheet11 = workbook.add_worksheet()
worksheet12 = workbook.add_worksheet()
currency_format = workbook.add_format({'num_format': '$#,##0'})
# Some sample data for the table.
data = [
    ['Apples', 10000, 5000, 8000, 6000],
    ['Pears', 2000, 3000, 4000, 5000],
    ['Bananas', 6000, 6000, 6500, 6000],
    ['Oranges', 500, 300, 200, 700],
]
########################################################################## # Example 1.
caption = 'Default table with no data.'
# Set the columns widths.
worksheet1.set_column('B:G', 12)
# Write the caption.
worksheet1.write('B1', caption)
# Add a table to the worksheet.
worksheet1.add_table('B3:F7')
########################################################################## # Example 2.
caption = 'Default table with data.'
# Set the columns widths.
worksheet2.set_column('B:G', 12)
# Write the caption.
worksheet2.write('B1', caption)
# Add a table to the worksheet.
worksheet2.add_table('B3:F7', {'data': data})
########################################################################## # Example 3.
caption = 'Table without default autofilter.'
# Set the columns widths.
worksheet3.set_column('B:G', 12)
# Write the caption.
worksheet3.write('B1', caption)
# Add a table to the worksheet.
worksheet3.add_table('B3:F7', {'autofilter': 0})
# Table data can also be written separately, as an array or individual cel
worksheet3.write_row('B4', data[0])
worksheet3.write_row('B5', data[1])
worksheet3.write_row('B6', data[2])
worksheet3.write_row('B7', data[3])
########################################################################## # Example 4.
caption = 'Table without default header row.'
# Set the columns widths.
worksheet4.set_column('B:G', 12)
# Write the caption.
worksheet4.write('B1', caption)
# Add a table to the worksheet.
worksheet4.add_table('B4:F7', {'header_row': 0})
# Table data can also be written separately, as an array or individual cel
worksheet4.write_row('B4', data[0])
worksheet4.write_row('B5', data[1])
worksheet4.write_row('B6', data[2])
worksheet4.write_row('B7', data[3])
########################################################################## # Example 5.
caption = 'Default table with "First Column" and "Last Column" options.'
# Set the columns widths.
worksheet5.set_column('B:G', 12)
# Write the caption.
worksheet5.write('B1', caption)
# Add a table to the worksheet.
worksheet5.add_table('B3:F7', {'first_column': 1, 'last_column': 1})
# Table data can also be written separately, as an array or individual cel
worksheet5.write_row('B4', data[0])
worksheet5.write_row('B5', data[1])
worksheet5.write_row('B6', data[2])
worksheet5.write_row('B7', data[3])
########################################################################## # Example 6.
caption = 'Table with banded columns but without default banded rows.'
# Set the columns widths.
worksheet6.set_column('B:G', 12)
# Write the caption.
worksheet6.write('B1', caption)
# Add a table to the worksheet.
worksheet6.add_table('B3:F7', {'banded_rows': 0, 'banded_columns': 1})
# Table data can also be written separately, as an array or individual cel
worksheet6.write_row('B4', data[0])
worksheet6.write_row('B5', data[1])
worksheet6.write_row('B6', data[2])
worksheet6.write_row('B7', data[3])
########################################################################## # Example 7.
caption = 'Table with user defined column headers'
# Set the columns widths.
worksheet7.set_column('B:G', 12)
# Write the caption.
worksheet7.write('B1', caption)
# Add a table to the worksheet.
worksheet7.add_table('B3:F7', {'data': data,
                               'columns': [{'header': 'Product'},
                                           {'header': 'Quarter 1'},
                                           {'header': 'Quarter 2'},
                                           {'header': 'Quarter 3'},
                                           {'header': 'Quarter 4'},
                                           ]})
caption = 'Table with user defined column headers'
# Set the columns widths.
worksheet8.set_column('B:G', 12)
# Write the caption.
worksheet8.write('B1', caption)
# Formula to use in the table.
formula = '=SUM(Table8[@[Quarter 1]:[Quarter 4]])'
# Add a table to the worksheet.
worksheet8.add_table('B3:G7', {'data': data,
                               'columns': [{'header': 'Product'},
                                           {'header': 'Quarter 1'},
                                           {'header': 'Quarter 2'},
                                           {'header': 'Quarter 3'},
                                           {'header': 'Quarter 4'},
                                           {'header': 'Year',
                                            'formula': formula},
                                           ]})
########################################################################## # Example 9.
caption = 'Table with totals row (but no caption or totals).'
# Set the columns widths.
worksheet9.set_column('B:G', 12)
# Write the caption.
worksheet9.write('B1', caption)
# Formula to use in the table.
formula = '=SUM(Table9[@[Quarter 1]:[Quarter 4]])'
# Add a table to the worksheet.
worksheet9.add_table('B3:G8', {'data': data,
                               'total_row': 1,
                               'columns': [{'header': 'Product'},
                                           {'header': 'Quarter 1'},
                                           {'header': 'Quarter 2'},
                                           {'header': 'Quarter 3'},
                                           {'header': 'Quarter 4'},
                                           {'header': 'Year',
                                            'formula': formula
                                            },
]})

caption = 'Table with totals row with user captions and functions.'
# Set the columns widths.
worksheet10.set_column('B:G', 12)
# Write the caption.
worksheet10.write('B1', caption)
# Options to use in the table.
options = {'data': data,
           'total_row': 1,
           'columns': [{'header': 'Product', 'total_string': 'Totals'},
                       {'header': 'Quarter 1', 'total_function': 'sum'},
                       {'header': 'Quarter 2', 'total_function': 'sum'},
                       {'header': 'Quarter 3', 'total_function': 'sum'},
                       {'header': 'Quarter 4', 'total_function': 'sum'},
                       {'header': 'Year',
                        'formula': '=SUM(Table10[@[Quarter 1]:[Quarter 4]])',
                        'total_function': 'sum'
                        },
]}
# Add a table to the worksheet.
worksheet10.add_table('B3:G8', options)
########################################################################## # Example 11.
caption = 'Table with alternative Excel style.'
# Set the columns widths.
worksheet11.set_column('B:G', 12)
# Write the caption.
worksheet11.write('B1', caption)
# Options to use in the table.
options = {'data': data,
           'style': 'Table Style Light 11',
           'total_row': 1,
           'columns': [{'header': 'Product', 'total_string': 'Totals'},
                       {'header': 'Quarter 1', 'total_function': 'sum'},
                       {'header': 'Quarter 2', 'total_function': 'sum'},
                       {'header': 'Quarter 3', 'total_function': 'sum'},
                       {'header': 'Quarter 4', 'total_function': 'sum'},
                       {'header': 'Year',
                        'formula': '=SUM(Table11[@[Quarter 1]:[Quarter 4]])','total_function': 'sum'
}, ]}
# Add a table to the worksheet.
worksheet11.add_table('B3:G8', options)
caption = 'Table with column formats.'
# Set the columns widths.
worksheet12.set_column('B:G', 12)
# Write the caption.
worksheet12.write('B1', caption)
# Options to use in the table.
options = {'data': data,
           'total_row': 1,
           'columns': [{'header': 'Product', 'total_string': 'Totals'},
                       {'header': 'Quarter 1',
                        'total_function': 'sum',
                        'format': currency_format,
                        },
                       {'header': 'Quarter 2',
                        'total_function': 'sum',
                        'format': currency_format,
                        },
                       {'header': 'Quarter 3',
                        'total_function': 'sum',
                        'format': currency_format,
                        },
                       {'header': 'Quarter 4',
                        'total_function': 'sum',
                        'format': currency_format,
                        },
                       {'header': 'Year',
                        'formula': '=SUM(Table12[@[Quarter 1]:[Quarter 4]])',
                        'total_function': 'sum',
                        'format': currency_format,
                        },
]}
# Add a table to the worksheet.
worksheet12.add_table('B3:G8', options)
workbook.close()
"""

"""
sparkline

workbook = xlsxwriter.Workbook('sparklines1.xlsx')
worksheet = workbook.add_worksheet()
data = [
    [-2, 2, 3, -1, 0],
    [30, 20, 33, 20, 15],
    [1, -1, -1, 1, -1],
]
worksheet.write_row('A1', data[0])
worksheet.write_row('A2', data[1])
worksheet.write_row('A3', data[2])

# Add a line sparkline (the default) with markers.
worksheet.add_sparkline('F1', {'range': 'Sheet1!A1:E1',
                               'markers': True})
# Add a column sparkline with non-default style.
worksheet.add_sparkline('F2', {'range': 'Sheet1!A2:E2',
                               'type': 'column',
                               'style': 12})
# Add a win/loss sparkline with negative values highlighted.
worksheet.add_sparkline('F3', {'range': 'Sheet1!A3:E3',
                               'type': 'win_loss',
                               'negative_points': True})
workbook.close()
"""

"""
comments

workbook = xlsxwriter.Workbook('comments1.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Hello')
worksheet.write_comment('A1', 'This is a comment')
workbook.close()

"""

"""
tab sheet设置颜色



import xlsxwriter
workbook = xlsxwriter.Workbook('tab_colors.xlsx')
# Set up some worksheets.
worksheet1 = workbook.add_worksheet()
worksheet2 = workbook.add_worksheet()
worksheet3 = workbook.add_worksheet()
worksheet4 = workbook.add_worksheet()
# Set tab colors
worksheet1.set_tab_color('red')
worksheet2.set_tab_color('green')
worksheet3.set_tab_color('#FF9900')  # Orange
# worksheet4 will have the default color.
workbook.close()
"""


"""chart2，带线标记
workbook = xlsxwriter.Workbook('chart2.xlsx')
worksheet = workbook.add_worksheet()
chart = workbook.add_chart({'type': 'column'})
# Write some data to add to plot on the chart.
data = [
    [1, 2, 3, 4, 5],
    [2, 4, 6, 8, 10],
    [3, 6, 9, 12, 15],
]
worksheet.write_column('A1', data[0])
worksheet.write_column('B1', data[1])
worksheet.write_column('C1', data[2])
# Configure the charts. In simplest case we just add some data series.
chart.add_series({'values': '=Sheet1!$A$1:$A$5'})
chart.add_series({'values': '=Sheet1!$B$1:$B$5'})
chart.add_series({'values': '=Sheet1!$C$1:$C$5'})
# Insert the chart into the worksheet.
worksheet.insert_chart('A7', chart)
workbook.close()
"""



"""
区域图

workbook = xlsxwriter.Workbook('chart_area.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
# Add the worksheet data that the charts will refer to.
headings = ['Number', 'Batch 1', 'Batch 2']


data = [
    [2, 3, 4, 5, 6, 7],
    [40, 40, 50, 30, 25, 50],
[30, 25, 30, 10, 5, 10],
]

worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
worksheet.write_column('C2', data[2])



chart1 = workbook.add_chart({'type': 'area'})
# Configure the first series.
chart1.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})
# Configure a second series. Note use of alternative syntax to define rang
chart1.add_series({
    'name':       ['Sheet1', 0, 2],
    'categories': ['Sheet1', 1, 0, 6, 0],
    'values':     ['Sheet1', 1, 2, 6, 2],
})
# Add a chart title and some axis labels.
chart1.set_title ({'name': 'Results of sample analysis'})
chart1.set_x_axis({'name': 'Test number'})
chart1.set_y_axis({'name': 'Sample length (mm)'})
# Set an Excel chart style.
chart1.set_style(11)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10}) ####################################################################### # Create a stacked area chart sub-type.
chart2 = workbook.add_chart({'type': 'area', 'subtype': 'stacked'})
# Configure the first series.
chart2.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})


chart2.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})
# Add a chart title and some axis labels.
chart2.set_title ({'name': 'Stacked Chart'})
chart2.set_x_axis({'name': 'Test number'})
chart2.set_y_axis({'name': 'Sample length (mm)'})
# Set an Excel chart style.
chart2.set_style(12)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D18', chart2, {'x_offset': 25, 'y_offset': 10}) #######################################################################
# Create a percent stacked area chart sub-type.
chart3 = workbook.add_chart({'type': 'area', 'subtype': 'percent_stacked'})
# Configure the first series.
chart3.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})
# Configure second series.
chart3.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})
# Add a chart title and some axis labels.
chart3.set_title ({'name': 'Percent Stacked Chart'})
chart3.set_x_axis({'name': 'Test number'})
chart3.set_y_axis({'name': 'Sample length (mm)'})
# Set an Excel chart style.
chart3.set_style(13)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D34', chart3, {'x_offset': 25, 'y_offset': 10})
workbook.close()


"""


"""
chart  bar2

workbook = xlsxwriter.Workbook('chart_bar2.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
# Add the worksheet data that the charts will refer to.
headings = ['Number', 'Batch 1', 'Batch 2']
data = [
    [2, 3, 4, 5, 6, 7],
    [10, 40, 50, 20, 10, 50],
    [30, 60, 70, 50, 40, 30],
]
worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
worksheet.write_column('C2', data[2])
####################################################################### # Create a new bar chart.
chart1 = workbook.add_chart({'type': 'bar'})
# Configure the first series.
chart1.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})
# Configure a second series. Note use of alternative syntax to define rang
chart1.add_series({
    'name':       ['Sheet1', 0, 2],
    'categories': ['Sheet1', 1, 0, 6, 0],
    'values':     ['Sheet1', 1, 2, 6, 2],
})
# Add a chart title and some axis labels.
chart1.set_title ({'name': 'Results of sample analysis'})
chart1.set_x_axis({'name': 'Test number'})
chart1.set_y_axis({'name': 'Sample length (mm)'})
# Set an Excel chart style.
chart1.set_style(11)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10}) ####################################################################### # Create a stacked chart sub-type.
chart2 = workbook.add_chart({'type': 'bar', 'subtype': 'stacked'})
# Configure the first series.
chart2.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})
# Configure second series.
chart2.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})
# Add a chart title and some axis labels.
chart2.set_title ({'name': 'Stacked Chart'})
chart2.set_x_axis({'name': 'Test number'})
chart2.set_y_axis({'name': 'Sample length (mm)'})
# Set an Excel chart style.
chart2.set_style(12)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D18', chart2, {'x_offset': 25, 'y_offset': 10})


chart3 = workbook.add_chart({'type': 'bar', 'subtype': 'percent_stacked'})
# Configure the first series.
chart3.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})
# Configure second series.
chart3.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})
# Add a chart title and some axis labels.
chart3.set_title ({'name': 'Percent Stacked Chart'})
chart3.set_x_axis({'name': 'Test number'})
chart3.set_y_axis({'name': 'Sample length (mm)'})
# Set an Excel chart style.
chart3.set_style(13)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D34', chart3, {'x_offset': 25, 'y_offset': 10})
workbook.close()

"""




"""

柱状图

workbook = xlsxwriter.Workbook('chart_column.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
# Add the worksheet data that the charts will refer to.
headings = ['Number', 'Batch 1', 'Batch 2']
data = [
    [2, 3, 4, 5, 6, 7],
    [10, 40, 50, 20, 10, 50],
    [30, 60, 70, 50, 40, 30],
]
worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
worksheet.write_column('C2', data[2])
####################################################################### # Create a new column chart.
chart1 = workbook.add_chart({'type': 'column'})
# Configure the first series.
chart1.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})
# Configure a second series. Note use of alternative syntax to define rang
chart1.add_series({
    'name':       ['Sheet1', 0, 2],
    'categories': ['Sheet1', 1, 0, 6, 0],
    'values':     ['Sheet1', 1, 2, 6, 2],
})
# Add a chart title and some axis labels.
chart1.set_title ({'name': 'Results of sample analysis'})
chart1.set_x_axis({'name': 'Test number'})
chart1.set_y_axis({'name': 'Sample length (mm)'})
# Set an Excel chart style.
chart1.set_style(11)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10}) ####################################################################### # Create a stacked chart sub-type.
chart2 = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
# Configure the first series.
chart2.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})
# Configure second series.
chart2.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})
# Add a chart title and some axis labels.
chart2.set_title ({'name': 'Stacked Chart'})
chart2.set_x_axis({'name': 'Test number'})
chart2.set_y_axis({'name': 'Sample length (mm)'})
# Set an Excel chart style.
chart2.set_style(12)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D18', chart2, {'x_offset': 25, 'y_offset': 10})
chart3 = workbook.add_chart({'type': 'column', 'subtype': 'percent_stacked'})
# Configure the first series.
chart3.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})
# Configure second series.
chart3.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})
# Add a chart title and some axis labels.
chart3.set_title ({'name': 'Percent Stacked Chart'})
chart3.set_x_axis({'name': 'Test number'})
chart3.set_y_axis({'name': 'Sample length (mm)'})
# Set an Excel chart style.
chart3.set_style(13)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D34', chart3, {'x_offset': 25, 'y_offset': 10})
workbook.close()

"""

"""折线图
workbook = xlsxwriter.Workbook('chart_line2.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
# Add the worksheet data that the charts will refer to.
headings = ['Number', 'Batch 1', 'Batch 2']
data = [
    [2, 3, 4, 5, 6, 7],
    [10, 40, 50, 20, 10, 50],
    [30, 60, 70, 50, 40, 30],
]
worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
worksheet.write_column('C2', data[2])
# Create a new chart object. In this case an embedded chart.
chart1 = workbook.add_chart({'type': 'line'})
# Configure the first series.
chart1.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})
chart1.add_series({
    'name':       ['Sheet1', 0, 2],
    'categories': ['Sheet1', 1, 0, 6, 0],
    'values':     ['Sheet1', 1, 2, 6, 2],
})
# Add a chart title and some axis labels.
chart1.set_title ({'name': 'Results of sample analysis'})
chart1.set_x_axis({'name': 'Test number'})
chart1.set_y_axis({'name': 'Sample length (mm)'})
# Set an Excel chart style. Colors with white outline and shadow.
chart1.set_style(10)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})
workbook.close()
"""



"""饼图
workbook = xlsxwriter.Workbook('chart_pie.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
# Add the worksheet data that the charts will refer to.
headings = ['Category', 'Values']
data = [
    ['Apple', 'Cherry', 'Pecan'],
    [60, 30, 10],
]
worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
####################################################################### # Create a new chart object.
chart1 = workbook.add_chart({'type': 'pie'})
chart1.add_series({
    'name':       'Pie sales data',
    'categories': ['Sheet1', 1, 0, 3, 0],
    'values':     ['Sheet1', 1, 1, 3, 1],
})
# Add a title.
chart1.set_title({'name': 'Popular Pie Types'})
# Set an Excel chart style. Colors with white outline and shadow.
chart1.set_style(10)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('C2', chart1, {'x_offset': 25, 'y_offset': 10})
#######################################################################
# Create a Pie chart with user defined segment colors. #
# Create an example Pie chart like above.
chart2 = workbook.add_chart({'type': 'pie'})
# Configure the series and add user defined segment colors.
chart2.add_series({
    'name': 'Pie sales data',
    'categories': '=Sheet1!$A$2:$A$4',
    'values':     '=Sheet1!$B$2:$B$4',
    'points': [
        {'fill': {'color': '#5ABA10'}},
        {'fill': {'color': '#FE110E'}},
        {'fill': {'color': '#CA5C05'}},
], })
# Add a title.
chart2.set_title({'name': 'Pie Chart with user defined colors'})
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('C18', chart2, {'x_offset': 25, 'y_offset': 10})
#######################################################################
# Create a Pie chart with rotation of the segments. #
# Create an example Pie chart like above.
chart3 = workbook.add_chart({'type': 'pie'})
# Configure the series.
chart3.add_series({
    'name': 'Pie sales data',
'categories': '=Sheet1!$A$2:$A$4',
    'values':     '=Sheet1!$B$2:$B$4',
})
# Add a title.
chart3.set_title({'name': 'Pie Chart with segment rotation'})
# Change the angle/rotation of the first segment.
chart3.set_rotation(90)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('C34', chart3, {'x_offset': 25, 'y_offset': 10})
workbook.close()

"""


"""甜甜圈图
workbook = xlsxwriter.Workbook('chart_doughnut.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
# Add the worksheet data that the charts will refer to.
headings = ['Category', 'Values']
data = [
    ['Glazed', 'Chocolate', 'Cream'],
    [50, 35, 15],
]
worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
####################################################################### # Create a new chart object.
chart1 = workbook.add_chart({'type': 'doughnut'})

chart1.add_series({
    'name':       'Doughnut sales data',
    'categories': ['Sheet1', 1, 0, 3, 0],
    'values':     ['Sheet1', 1, 1, 3, 1],
})
# Add a title.
chart1.set_title({'name': 'Popular Doughnut Types'})
# Set an Excel chart style. Colors with white outline and shadow.
chart1.set_style(10)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('C2', chart1, {'x_offset': 25, 'y_offset': 10})
#######################################################################
# Create a Doughnut chart with user defined segment colors. #
# Create an example Doughnut chart like above.
chart2 = workbook.add_chart({'type': 'doughnut'})
# Configure the series and add user defined segment colors.
chart2.add_series({
    'name': 'Doughnut sales data',
    'categories': '=Sheet1!$A$2:$A$4',
    'values':     '=Sheet1!$B$2:$B$4',
    'points': [
        {'fill': {'color': '#FA58D0'}},
        {'fill': {'color': '#61210B'}},
        {'fill': {'color': '#F5F6CE'}},
], })
# Add a title.
chart2.set_title({'name': 'Doughnut Chart with user defined colors'})
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('C18', chart2, {'x_offset': 25, 'y_offset': 10})
#######################################################################
# Create a Doughnut chart with rotation of the segments. #
# Create an example Doughnut chart like above.
chart3 = workbook.add_chart({'type': 'doughnut'})
# Configure the series.
chart3.add_series({
    'name': 'Doughnut sales data',
 'categories': '=Sheet1!$A$2:$A$4',
    'values':     '=Sheet1!$B$2:$B$4',
})
# Add a title.
chart3.set_title({'name': 'Doughnut Chart with segment rotation'})
# Change the angle/rotation of the first segment.
chart3.set_rotation(90)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('C34', chart3, {'x_offset': 25, 'y_offset': 10})
#######################################################################
# Create a Doughnut chart with user defined hole size and other options. #
# Create an example Doughnut chart like above.
chart4 = workbook.add_chart({'type': 'doughnut'})
# Configure the series.
chart4.add_series({
    'name': 'Doughnut sales data',
    'categories': '=Sheet1!$A$2:$A$4',
    'values':     '=Sheet1!$B$2:$B$4',
    'points': [
        {'fill': {'color': '#FA58D0'}},
        {'fill': {'color': '#61210B'}},
        {'fill': {'color': '#F5F6CE'}},
], })
# Set a 3D style.
chart4.set_style(26)
# Add a title.
chart4.set_title({'name': 'Doughnut Chart with options applied'})
# Change the angle/rotation of the first segment.
chart4.set_rotation(28)
# Change the hole size.
chart4.set_hole_size(33)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('C50', chart4, {'x_offset': 25, 'y_offset': 10})
workbook.close()
"""


workbook = xlsxwriter.Workbook('chart_scatter.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
# Add the worksheet data that the charts will refer to.
headings = ['Number', 'Batch 1', 'Batch 2']
data = [
    [2, 3, 4, 5, 6, 7],
    [10, 40, 50, 20, 10, 50],
    [30, 60, 70, 50, 40, 30],
]
worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
worksheet.write_column('C2', data[2])
####################################################################### # Create a new scatter chart.
chart1 = workbook.add_chart({'type': 'scatter'})
# Configure the first series.
chart1.add_series({
    'name': '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
'values': '=Sheet1!$B$2:$B$7',
})
# Configure second series. Note use of alternative syntax to define ranges
chart1.add_series({
    'name':       ['Sheet1', 0, 2],
    'categories': ['Sheet1', 1, 0, 6, 0],
    'values':     ['Sheet1', 1, 2, 6, 2],
})
# Add a chart title and some axis labels.
chart1.set_title ({'name': 'Results of sample analysis'})
chart1.set_x_axis({'name': 'Test number'})
chart1.set_y_axis({'name': 'Sample length (mm)'})
# Set an Excel chart style.
chart1.set_style(11)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})
#######################################################################
#  Create a scatter chart sub-type with straight lines and markers.
chart2 = workbook.add_chart({'type': 'scatter',
                             'subtype': 'straight_with_markers'})
# Configure the first series.
chart2.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})
# Configure second series.
chart2.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})
# Add a chart title and some axis labels.
chart2.set_title ({'name': 'Straight line with markers'})
chart2.set_x_axis({'name': 'Test number'})
chart2.set_y_axis({'name': 'Sample length (mm)'})
# Set an Excel chart style.
chart2.set_style(12)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D18', chart2, {'x_offset': 25, 'y_offset': 10})

chart3 = workbook.add_chart({'type': 'scatter', 'subtype': 'straight'})
# Configure the first series.
chart3.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})
# Configure second series.
chart3.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})
# Add a chart title and some axis labels.
chart3.set_title ({'name': 'Straight line'})
chart3.set_x_axis({'name': 'Test number'})
chart3.set_y_axis({'name': 'Sample length (mm)'})
# Set an Excel chart style.
chart3.set_style(13)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D34', chart3, {'x_offset': 25, 'y_offset': 10})
#######################################################################
#  Create a scatter chart sub-type with smooth lines and markers.
chart4 = workbook.add_chart({'type': 'scatter',
                             'subtype': 'smooth_with_markers'})
# Configure the first series.
chart4.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})
# Configure second series.
chart4.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

chart4.set_title ({'name': 'Smooth line with markers'})
chart4.set_x_axis({'name': 'Test number'})
chart4.set_y_axis({'name': 'Sample length (mm)'})
# Set an Excel chart style.
chart4.set_style(14)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D50', chart4, {'x_offset': 25, 'y_offset': 10})
#######################################################################
#  Create a scatter chart sub-type with smooth lines and no markers.
chart5 = workbook.add_chart({'type': 'scatter',
                             'subtype': 'smooth'})
# Configure the first series.
chart5.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})
# Configure second series.
chart5.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})
# Add a chart title and some axis labels.
chart5.set_title ({'name': 'Smooth line'})
chart5.set_x_axis({'name': 'Test number'})
chart5.set_y_axis({'name': 'Sample length (mm)'})
# Set an Excel chart style.
chart5.set_style(15)
# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D66', chart5, {'x_offset': 25, 'y_offset': 10})
workbook.close()