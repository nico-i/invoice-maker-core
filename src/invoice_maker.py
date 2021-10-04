# -*- coding: utf-8 -*-
import os
import sys
from datetime import date, datetime, timedelta

from bs4 import BeautifulSoup as bs
from pyasn1.type.univ import Null
from cal_setup import get_calendar_service
from weasyprint import CSS, HTML

from events import get_events

print('--- Invoice-Maker ---\nWritten by Nico Ismaili-\nContact: nico@ismaili.de\nWeb: nico.ismaili.de')
print('\n- Start -\n')
# see 'Python Quickstart' in 'Google Docs for Developers' for more infos on service
service = get_calendar_service()

print('1. Creating HTML Template.')

# Base path to this dir
base_path = os.path.dirname(os.path.abspath(__file__).replace('src\\', ''))
# generate default absolute paths from relative ones and base_path
invoice_html_file_path = os.path.join(base_path, './resource/invoice.html')
css_file_path = os.path.join(base_path, './resource/css/style.css')
tmp_html_path = os.path.join(base_path, './resource/output/tmp.html')
output_file_path = os.path.join(base_path, './resource/output/invoice.pdf')
config_path = os.path.join(base_path, './resource/data/config.txt')
static_values_path = os.path.join(
    base_path, './resource/data/static_values.txt')
messages_path = os.path.join(base_path, './resource/data/messages.txt')
# default start and end dates
end_date = date.today()
start_date = end_date - timedelta(days=(date.today().replace(day=1) - timedelta(days=1)).day)
# initialize soup
soup = any
with open(invoice_html_file_path, encoding='utf-8') as txt_file:
    soup = bs(txt_file, 'html.parser', from_encoding='utf-8')
# initalize messages_dic
messages_dic = {}
with open(messages_path, encoding='utf-8') as txt_file:
    messages_dic = {x[0]: x[1] for x in [y.strip().split('=')
                                         for y in txt_file.readlines()]}
# fill soup with messages_dic
for key in messages_dic.keys():
    soup.find('span', {'id': key}).string = messages_dic.get(key, '')
# initalize static_dic
static_dic = {}
with open(static_values_path, encoding='utf-8') as txt_file:
    static_dic = {x[0]: x[1] for x in [y.strip().split('=')
                                       for y in txt_file.readlines()] if x[1] != ''}
# if static_values.txt hasn't been modified use mock data
if len(static_dic) == 0:
    with open(os.path.join(base_path, './resource/mock/static_values.txt'), encoding='utf-8') as txt_file:
        static_dic = {x[0]: x[1] for x in [y.strip().split('=') for y in txt_file.readlines()] if x[1] != ''}
# update some values dynamically
static_dic.update({'MONTH_YEAR': datetime.today().strftime('%m/%Y')})
hour_rate = 0
if(not static_dic.get('HOURLY_RATE', 0) == ""):
    hour_rate = float(static_dic.get('HOURLY_RATE', 0))
static_dic.update({'HOURLY_RATE': '{0:.2f}'.format(float(hour_rate)) + ' €'})
static_dic.update({'TODAY': datetime.today().strftime('%d.%m.%Y')})
# fill soup with messages_dic
for key in static_dic.keys():
    soup.find('span', {'id': key}).string = static_dic.get(key, '')
# initalize config_dic
config_dic = {}
with open(config_path, encoding='utf-8') as f2:
    config_dic = {x[0]: x[1] for x in [y.strip().split('=')
                                       for y in f2.readlines()] if x[1] != ''}
# if config.txt hasn't been modified use mock data
if len(config_dic) == 0:
    with open(os.path.join(base_path, './resource/mock/config.txt'), encoding='utf-8') as txt_file:
        config_dic = {x[0]: x[1] for x in [y.strip().split('=') for y in txt_file.readlines()]}
# update start and end dates if PAYDAY was defined
if(config_dic.get('PAYDAY', '') != ''):
    end_date = date.today().replace(day=int(config_dic.get('PAYDAY')))
    start_date = end_date - \
        timedelta(days=(date.today().replace(day=1) - timedelta(days=1)).day)
# initialise values to be calculated later
events = get_events(service, config_dic.get('CAL_ID', ''), start_date, end_date)
max_hours = config_dic.get('MAX_HOURS', 0)
if(max_hours == ""):
    max_hours = 0
else:
    max_hours = float(max_hours)
overtime = 0
total_hours = 0
hours_to_payout = 0
# go through events and fill table in soup
for x in events:
    tr_tag = soup.new_tag('tr')
    total_hours += x[3]
    for y in x:
        td_tag = soup.new_tag('td')
        td_tag.string = str(y)
        tr_tag.append(td_tag)
    soup.find('table', {'id': 'CALC_TABLE'}).append(tr_tag)

print('4. Calculating payout and overtime.\n5. Filling template with dynamic values.')

overtime_last_month = 0
if(config_dic.get('OVERTIME_PREV_MONTH', '') != ''):
    overtime_last_month = float(config_dic.get('OVERTIME_PREV_MONTH'))
overtime = total_hours - max_hours
config_dic.update({'H_MONTH': str(total_hours)})
# check if total_hours is larger than max_hours and adjust overtime accordingly
if(total_hours > max_hours):
    hours_to_payout = total_hours - overtime
    config_dic.update({'H_TO_PAY': str(hours_to_payout)})
    config_dic.update({'OVERTIME_REST': str(overtime_last_month+overtime)})
else:
    if(total_hours + overtime_last_month < max_hours):
        hours_to_payout = total_hours + overtime_last_month
        config_dic.update({'H_TO_PAY': str(hours_to_payout)})
        config_dic.update({'OVERTIME_REST': str(0)})
    else:
        hours_to_payout = total_hours + overtime_last_month
        config_dic.update({'H_TO_PAY': str(hours_to_payout)})
        config_dic.update({'OVERTIME_REST': str(
            max_hours - total_hours + overtime_last_month)})
# if script was called with 'py invoice_maker.py 1' add total_hours to ALL_HOURS
if(len(sys.argv) == 2 and int(sys.argv[1]) == 1):
    config_dic.update({'ALL_H': str(float(config_dic.get('ALL_H', 0))+total_hours)})
config_dic.update({'LOAN': '{0:.2f}'.format(hours_to_payout*hour_rate) + ' €'})
# fill soup with config_dic
for key in list(config_dic.keys())[4:]:
    soup.find('span', {'id': key}).string = config_dic.get(key, '')
# if script was called with 'py invoice_maker.py 1' overwrite OVERTIME_PREV_MONTH and ALL_H in dyn_values.txt
if(len(sys.argv) == 2 and int(sys.argv[1]) == 1):
    with open(config_dic, 'w') as txt_file:
        txt_file.write('OVERTIME_PREV_MONTH' + '=' +
                       str(config_dic.get('OVERTIME_REST', 0)) + '\n')
        txt_file.write('ALL_H' + '=' + str(config_dic.get('ALL_H', 0)))
# generate temporary html file from soup
with open(tmp_html_path, 'wb') as html_file:
    html_file.write(soup.prettify('utf-8'))

print('6. Parsing HTML to PDF.')
# create pdf from temporary html
if(not config_dic.get('OUTPUT_PDF_PATH', '') == ''):
    output_file_path = config_dic.get('OUTPUT_PDF_PATH', '')
HTML(tmp_html_path).write_pdf(
    output_file_path, stylesheets=[CSS(css_file_path)])

os.remove(tmp_html_path)

print('\n- Finish -\n')
