import time

from tvDatafeed import TvDatafeed, Interval

username = 'chetancindia857'
password = 'Abc@123'

tv = TvDatafeed()

# index
def getdata():
    niftydara =  tv.get_hist(symbol='NIFTY',exchange='NSE',interval=Interval.in_5_minute,n_bars=100)
    print((niftydara))

while True:
    getdata()
    time.sleep(0.5)