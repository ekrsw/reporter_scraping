import datetime
import time
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select


class Reader(object):
    def __init__(self, name, operator_id, URL, driver_path):
        self.name = name
        self.URL = URL
        self.operator_id = operator_id
        self.driver_path = driver_path

    def scrape_reporter(self, template_name):
        options = Options()
        options.add_argument('--headless')

        driver = webdriver.Chrome(executable_path=self.driver_path, options=options)
        driver.implicitly_wait(5)

        driver.get(self.URL)

        # ログインIDを入力してログイン
        input_operator_id = driver.find_element_by_id('logon-operator-id')
        input_operator_id.send_keys(self.operator_id)
        driver.find_element_by_id('logon-btn').click()

        # テンプレート呼び出し
        driver.find_element_by_id('template-title-span').click()
        el = driver.find_element_by_id('template-download-select')
        s = Select(el)
        s.select_by_value(template_name)
        driver.find_element_by_id('template-creation-btn').click()

        time.sleep(1)
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, 'lxml')

        base_id = 'normal-list1-dummy-0-table-body-table'

        logon_time = soup.find(id='{}-{}-{}'.format(base_id, 0, 1)).string
        incoming_time = soup.find(id='{}-{}-{}'.format(base_id, 0, 2)).string
        outgoing_time = soup.find(id='{}-{}-{}'.format(base_id, 0, 3)).string
        work_time = soup.find(id='{}-{}-{}'.format(base_id, 0, 4)).string
        af_incoming = soup.find(id='{}-{}-{}'.format(base_id, 0, 5)).string
        af_outgoing = soup.find(id='{}-{}-{}'.format(base_id, 0, 6)).string

        driver.quit()

        return logon_time, incoming_time, outgoing_time, work_time, af_incoming, af_outgoing

    def read_shift(self, name, shift_filename, sheet_name, start_date, end_date):
        df = pd.read_excel(shift_filename, skiprows=12, index_col=1, sheet_name=sheet_name)
        df = df.iloc[:,2:].T
        print(df)
        dates = pd.date_range(start_date, end_date, freq='D')
        print(dates)
        df.index = dates
        return df[name]

if __name__ == '__main__':
    import os

    name = '正村憲一ＳＶ'
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

    report_filename = '202206_業務報告v4_是澤.xlsx'
    report_filepath = os.path.join(report_path, report_filename)
    shift_filename = '46期CSCシフト表.xlsx'
    sheet_name = '2022.9-10'
    start_date = '2022-09-01'
    end_date = '2022-10-31'
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    
    reader = Reader(name, operator_id, URL, driver_path)
    shift_data = reader.read_shift(name, shift_filename, sheet_name, start_date, end_date)
    t_shift = shift_data[today.strftime('%Y-%m-%d')]
    y_shift = shift_data[yesterday.strftime('%Y-%m-%d')]

    print(t_shift, y_shift)

    if y_shift == '22_8':
        template_name = '日報（昨日）'
    else:
        template_name = '日報（本日）'
    
    (logon_time,
    incoming_time,
    outgoing_time,
    work_time,
    af_incoming,
    af_outgoing)\
        = reader.scrape_reporter(template_name)

    print(logon_time, incoming_time, outgoing_time, work_time, af_incoming, af_outgoing)