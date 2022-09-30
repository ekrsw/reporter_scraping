import datetime

from reader import Reader
from writer import Writer
from calc import Calulator
import pandas as pd
import os
import sys

name = '是澤英輔'
operator_id = 'eisuke_koresawa'
URL = 'http://sccts7dxsql/ctreport'
driver_path = 'C:\\driver\\chromedriver.exe'
template_name = '日報（本日）'

debug = False
if not debug:
    report_path = '\\\\mjs.co.jp\\datas\\CSC共有フォルダ\\第46期 東京CSC第二グループ\\46期日次_月次報告\\髙木\\是澤\\'
elif debug:
    report_path = ''
else:
    raise ValueError

report_filename = '202209_業務報告v4_是澤.xlsx'
report_filepath = os.path.join(report_path, report_filename)
shift_filename = '46期CSCシフト表.xlsx'
sheet_name = '2022.9-10'
start_date = '2022-09-01'
end_date = '2022-10-31'
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

# インスタンス作成
reader = Reader(name, operator_id, URL, driver_path)
writer = Writer()
calculator = Calulator()

# シフトデータを読み込んでt_shiftとy_shiftを作成
shift_data = reader.read_shift(name, shift_filename, sheet_name, start_date, end_date)
t_shift = shift_data[today.strftime('%Y-%m-%d')]
y_shift = shift_data[yesterday.strftime('%Y-%m-%d')]

print(t_shift, y_shift)

# y_shiftが夜勤のときは昨日のレポータをスクレイピングする
if y_shift == '22_8':
    template_name = '日報（昨日）'
    is_nightshift = True
else:
    template_name = '日報（本日）'
    is_nightshift = False
    
(logon_time,
incoming_time,
outgoing_time,
work_time,
af_incoming,
af_outgoing)\
    = reader.scrape_reporter(template_name)

work_total = calculator.calc_work_total(work_time, af_incoming, af_outgoing)

print(logon_time)
print(incoming_time)
print(outgoing_time)
print(work_total)

today_shift = shift_data[today.strftime('%Y-%m-%d')]
w_hours, core_time = calculator.calc_wh(logon_time, today_shift)

print(report_filepath)
writer.write_shift(is_nightshift, today_shift, report_filepath, w_hours, core_time, incoming_time, outgoing_time, work_total)
