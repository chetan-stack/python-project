

from smartapi import SmartConnect
import time
from datetime import datetime,timedelta
import datetime
import pandas_ta as ta
import pandas as pd
import numpy as np
import os
import sys
import pyotp


api_key = "pMZtYR5S"
user_id = "c182721"
password = "Csethi@4321"
totp = pyotp.TOTP("ELAC7LJCYC6ENWQBWNEGRGV66U").now()

current_date_time = datetime.datetime.now()
form_date = current_date_time - timedelta(days = 30)

script_list = {
    'ADANIENT-EQ': '25',
    'APOLLOHOSP-EQ': '157',
    'ASIANPAINT-EQ': '236',
    'AXISBANK-EQ': '5900',
    'BAJFINANCE-EQ': '317',
    'BAJAJFINSV-EQ': '16675',
    'BPCL-EQ': '526',
    'BHARTIARTL-EQ': '10604',
    'BRITANNIA-EQ': '547',
    'CIPLA-EQ': '694',
    'COALINDIA-EQ': '20374',
    'DIVISLAB-EQ': '10940',
    'DRREDDY-EQ': '881',
    'EICHERMOT-EQ': '910',
    'GRASIM-EQ': '1232',
    'HCLTECH-EQ': '7229',
    'HDFCBANK-EQ': '1333',
    'HDFCLIFE-EQ': '467',
    'HEROMOTOCO-EQ': '1348',
    'HINDALCO-EQ': '1363',
    'HINDUNILVR-EQ': '1394',
    'HDFC-EQ': '1330',
    'ICICIBANK-EQ': '4963',
    'ITC-EQ': '1660',
    'INDUSINDBK-EQ': '5258',
    'INFY-EQ': '1594',
    'JSWSTEEL-EQ': '11723',
    'KOTAKBANK-EQ': '1922',
    'M&M-EQ': '2031',
    'MARUTI-EQ': '10999',
    'NTPC-EQ': '11630',
    'NESTLEIND-EQ': '17963',
    'ONGC-EQ': '2475',
    'POWERGRID-EQ': '14977',
    'RELIANCE-EQ': '2885',
    'SBILIFE-EQ': '21808',
    'SBIN-EQ': '3045',
    'SUNPHARMA-EQ': '3351',
    'TCS-EQ': '11536',
    'TATACONSUM-EQ': '3432',
    'TATAMOTORS-EQ': '3456',
    'TATASTEEL-EQ': '3499',
    'TECHM-EQ': '13538',
    'TITAN-EQ': '3506',
    'UPL-EQ': '11287',
    'ULTRACEMCO-EQ': '11532',
    'WIPRO-EQ': '3787',
  };

buy_traded_stock = []
sell_traded_stock = []

exchange = "NSE"
per_trade_fund = 10000
ma_short = 13
ma_long = 22
runcount = 0

def GettingLtpData(script, token, order):
    LTP = obj.ltpData(exchange, script, token)
#     print(LTP)
    ltp = LTP["data"]["ltp"]
    quantity = int(per_trade_fund / ltp)
    orderparams = {
        "variety": "NORMAL",
        "tradingsymbol": script,
        "symboltoken": token,
        "transactiontype": order,
        "exchange": exchange,
        "ordertype": "LIMIT",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "price": ltp,
        "squareoff": "0",
        "stoploss": "0",
        "quantity": quantity
    }
    orderId = obj.placeOrder(orderparams)
    print(
        f"{order} order Place for {script} at : {datetime.datetime.now()} with Order id {orderId}"
    )

def strategy():
    global obj

    obj = SmartConnect(api_key=api_key)
    token = obj.generateToken(obj.generateSession(user_id, password,totp)["data"]["refreshToken"])
    jwtToken = token['data']["jwtToken"]
    refreshToken = token['data']['refreshToken']
    feedToken = token['data']['feedToken']
#     print(feedToken)
    try:
        for script, token in script_list.items():
            historicParam = {
                "exchange": exchange,
                "symboltoken": token,
                "interval": "FIFTEEN_MINUTE",
                "fromdate": form_date.strftime("%Y-%m-%d 09:15"), 
                "todate": current_date_time.strftime("%Y-%m-%d %H:%M")
            }
            hist_data = obj.getCandleData(historicParam)["data"]
#             print(hist_data)
            if hist_data != None:
                df = pd.DataFrame(
                    hist_data,
                    columns=['date', 'open', 'high', 'low', 'close', 'volume'])
                df["sup"] = ta.supertrend(df['high'], df['low'], df['close'], length=7, multiplier=3)['SUPERT_7_3.0']

                df.dropna(inplace=True)
                # print(df)
                # close price
                sup_cl = df.sup.values[-1]
                close_cl = df.close.values[-1]
                # pre close
                sup_pre = df.sup.values[-2]
                close_pre = df.close.values[-2]

                if not df.empty:
                    if close_pre >= sup_pre and close_cl < sup_cl and (script not in sell_traded_stock):
                        sell_traded_stock.append(script)
                        print(script,token, "SELL")
#                         GettingLtpData(script, token, "SELL")

                    if close_pre <= sup_pre and close_cl > sup_cl and (script not in buy_traded_stock):
                        buy_traded_stock.append(script)
                        print(script,token, "BUY")
#                         GettingLtpData(script, token, "BUY")

#                 print("complete",traded_stock)  
            time.sleep(0.5)

    except Exception as e:
        print("Historic Api failed: {}".format(e))
    try:
        logout = obj.terminateSession(user_id)
        print("Logout Successfull")
    except Exception as e:
        print("Logout failed: {}".format(e))

def main():
    global runcount
    start_time = int(9) * 60 + int(20)
    end_time = int(15) * 60 + int(10)
    stop_time = int(15) * 60 + int(15)
    last_time = start_time
    schedule_interval = 60*5
    print("start")
    while True:
        if (datetime.datetime.now().hour * 60 +
                datetime.datetime.now().minute) >= end_time:
            if (datetime.datetime.now().hour * 60 +
                    datetime.datetime.now().minute) >= stop_time:
                print(sys._getframe().f_lineno,
                      "Trading is closed, time is above 03:15 PM")
                break

        elif (datetime.datetime.now().hour * 60 +
              datetime.datetime.now().minute) >= start_time:
            if time.time() >= last_time:
                last_time = time.time() + schedule_interval
                print(f"{runcount} Run Count : Time - {datetime.datetime.now()}")
                if runcount >= 0:
                    try:
                        strategy()
                    except Exception as e:
                        print("Run error", e)
                runcount = runcount + 1
        else:
            print(f'Waiting...strategy will start working at 09:20 AM')
            time.sleep(1)

if (__name__ == '__main__'):
#     print("lets start")
    main()