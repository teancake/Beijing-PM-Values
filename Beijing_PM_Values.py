import requests
from dateutil.parser import parse

def get_beijing_pm_values():
    # data interface of Beijing Municipal Environmental Monitoring Center
    url = 'http://zx.bjmemc.com.cn/web/Service.ashx'
    # connection time out value
    time_out = 10
    # http header
    http_header = {
    'Host': 'zx.bjmemc.com.cn',
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

    # http request 
    res = requests.get(url, headers = http_header, timeout=time_out)
    # the data is in JSON format
    data = res.json()
    tbl = data['Table']
    # search for PM2.5 and PM10 value
    for i in range(len(tbl)):
        tmp = tbl[i]
        if tmp['Pollutant'] == 'PM2.5':
            pm2_5 = int(tmp['Value'])
            date_time = tmp['Date_Time']
        if tmp['Pollutant'] == 'PM10':
            pm10 = int(tmp['Value'])
            date_time = tmp['Date_Time']
    # parse date and time in the data record
    dt = parse(date_time)
    date = dt.date()
    time = dt.time()
    return date, time, pm2_5, pm10


date, time, pm2_5, pm10 = get_beijing_pm_values()
print(date, time, pm2_5, pm10)

