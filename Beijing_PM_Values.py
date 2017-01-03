#!/usr/bin/env python
# get Beijing air quality values

import requests
import dateutil.parser
import xml.etree.ElementTree as ET
import time

# Get data from the U.S. Embassy Beijing Air Quality Monitor
def get_beijing_pm_values_from_us_emb(http_header, time_out):
    # data interface of the U.S Embassy Beijing Air Quality Monitor
    url = 'http://www.stateair.net/web/rss/1/1.xml'
    # add host info the the http header
    http_header['Host'] = 'www.stateair.net'
    try:
        # http request 
        res = requests.get(url, headers = http_header, timeout=time_out)
        # parse xml content
        xmlroot = ET.fromstring(res.content)
        # find the PM2.5 value
        pm2_5 = xmlroot.find('channel/item/Conc').text
        pm10 = 'N/A'
        # parse date and time in the data record
        dt = dateutil.parser.parse(xmlroot.find('channel/item/ReadingDateTime').text)
        cur_date = dt.date()
        cur_time = dt.time()
        status = 0
    except:
        status = -1
        cur_date = 'N/A' 
        cur_time = 'N/A' 
        pm2_5 = 'N/A'
        pm10 = 'N/A'
    return cur_date, cur_time, pm2_5, pm10, status

# Get data from Beijing Municipal Environmental Monitoring Center
def get_beijing_pm_values(http_header, time_out):
    # data interface of Beijing Municipal Environmental Monitoring Center
    url = 'http://zx.bjmemc.com.cn/web/Service.ashx'
    # add host info the the http header
    http_header['Host']='zx.bjmemc.com.cn'
    try:
        # http request 
        res = requests.get(url, headers = http_header, timeout=time_out)
        # the data is in JSON format
        data = res.json()
        tbl = data['Table']
        # search for PM2.5 and PM10 value
        for i in range(len(tbl)):
            tmp = tbl[i]
            if tmp['Pollutant'] == 'PM2.5':
                if(tmp['Value']!=''):
                    pm2_5 = tmp['Value']
                else:
                    pm2_5 = 'N/A'
                date_time = tmp['Date_Time']
            if tmp['Pollutant'] == 'PM10':
                if (tmp['Value']!=''):
                    pm10 = tmp['Value']
                else:
                    pm10 = 'N/A'
                date_time = tmp['Date_Time']
        # parse date and time in the data record
        dt = dateutil.parser.parse(date_time)
        cur_date = dt.date()
        cur_time = dt.time()
        status = 0
    except:
        status = -1
        cur_date = 'N/A' 
        cur_time = 'N/A' 
        pm2_5 = 'N/A'
        pm10 = 'N/A'
    return cur_date, cur_time, pm2_5, pm10, status

# Connection parameters
# time out value
time_out = 10
# http header
http_header = {
# firefox
#'User-Agent': 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
# chrome/safari
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
# firefox
#'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
# chrome/safari
'Accept': 'application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5',
# Note: the Accept-Encoding line could be removed, in which case uncompressed 
# data is transferred and the amount of data transferred will be increased.
# If this option is used, then the data should be uncompress before being used.
'Accept-Encoding': 'gzip, deflate',
'Connection': 'keep-alive'}

date, time, pm2_5, pm10, status = get_beijing_pm_values(http_header, time_out)
print(status, date, time, pm2_5, pm10)

date, time, pm2_5, pm10, status = get_beijing_pm_values_from_us_emb(http_header, time_out)
print(status, date, time, pm2_5, pm10)
