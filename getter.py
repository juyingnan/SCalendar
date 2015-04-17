__author__ = 'bunny_gg'
import urllib2
import json
import time
import datetime


def json_string_load(json_string):
    return json.loads(json_string)


def secret(date, hour):
    lastDate = date - datetime.timedelta(days=1)
    nextDate = date + datetime.timedelta(days=1)
    # print lastDate

    # get data (string) from internet
    http_url = "http://api.worldweatheronline.com/free/v2/past-weather.ashx?key=2757c7ea4cf4331de52aac5f9ebc2&q=beijing&date=" + lastDate.__str__() + "&enddate="+ nextDate.__str__() +"&tp=1&format=json"
    response = urllib2.urlopen(http_url).read()
    # print response
    # for Python 3.x
    # import urllib.request
    # urllib.request.urlopen("http://example.com/foo/bar").read()


    # convert string to json / dict
    response_json = json_string_load(response)
    # print response_json

    # get all pressure data
    key = "pressure"
    offset = -4
    pressure = []
    pressure_no_offset = []
    humidity = []
    # time_list = []
    # tempC = []
    for day in response_json["data"]["weather"]:
        for hourly in day["hourly"]:
            # print hourly[key]
            # pressure.append(int(hourly[key]))
            pressure.append(int(hourly[key]) + offset)
            pressure_no_offset.append(int(hourly[key]))
            humidity.append(int(hourly["humidity"]))
            # time_list.append(int(hourly["time"]))
            # tempC.append(int(hourly["tempC"]))
    # print pressure

    max_index = pressure.index(max(pressure))
    min_index = pressure.index(min(pressure))
    trend = [0]
    trend_index = 0.7
    for i in range(1,len(pressure)-1):
        trend.append((pressure[i+1] - pressure[i]) * trend_index +(pressure[i] - pressure[i-1]) * (1-trend_index))
    trend[0] = trend[1] * trend_index
    trend.append(trend[len(trend)-1] * trend_index)
    # print trend
    # print hour
    count_per_day = 8
    point = int(( hour + 1 ) / 3) + count_per_day
    if pressure[point] > 1003 and trend[point] >=0:
        result = True
    else:
        result = False
    if pressure[point] >= 1015:
        result = True
    # else:
    #    result = False
    cal_aqi = 6951.32 + 3.1128 * humidity[point] - 6.79088 * pressure_no_offset[point]
    print result, date, hour ,":" "Current Pressure: ", pressure[point], ":", "Current Trend: ", trend[point], "Cal AQI: ", cal_aqi
    return result

# get time
# localtime = time.localtime(time.time())
# print time.strftime('%Y-%m-%d',time.localtime(time.time()))
date=datetime.date.today()
localtime = time.localtime(time.time())
secret(date, localtime.tm_hour)

# test
for i in range(55,50,-1):
    lastDate = date - datetime.timedelta(days=i)
    for i in range(0,24,1):
            secret(lastDate, i)

