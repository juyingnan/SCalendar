__author__ = 'bunny_gg'
import time

localtime = time.localtime(time.time())
print localtime.tm_hour
point = int(( localtime.tm_hour + 1 ) / 3)
