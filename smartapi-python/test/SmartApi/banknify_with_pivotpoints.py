
from SmartApi import SmartConnect #or from SmartApi.smartConnect import SmartConnect
import time
from datetime import datetime,timedelta
import datetime
import pandas_ta as ta
import pandas as pd
import numpy as np
import os
import sys
import pyotp
import schedule
import math
import requests
import document
import time
from tvDatafeed import TvDatafeed, Interval


api_key = document.api_key
user_id = document.user_id
password = document.password
totp = pyotp.TOTP(document.totp).now()
obj = SmartConnect(api_key=api_key)
token = obj.generateToken(obj.generateSession(user_id, password, totp)["data"]["refreshToken"])

current_date_time = datetime.datetime.now() - timedelta(days = 1)
form_date = current_date_time - timedelta(days = 10)
traded_list_exit = []
print("current tym",current_date_time)
placeOREDR = True
script_list = {
    "BAJAJFINSV-EQ": "16675",
    'HDFCBANK-EQ': '1333',
    'TITAN-EQ': '3506',
    'HDFCLIFE-EQ': '467',
    'ICICIBANK-EQ': '4963',
    'JSWSTEEL-EQ': '11723',
    'TATASTEEL-EQ': '3499',
    'INFY-EQ': '1594',
    "ITC-EQ": "1660",
    "WIPRO-EQ": "3787",
    'RELIANCE-EQ': '2885',
    'TCS-EQ': '11536',

};
buy_traded_stock = []
sell_traded_stock = []

exchange = "NSE"
per_trade_fund = 10000
ma_short = 13
ma_long = 22
runcount = 0
selltradednity = []
buytradedBANKNIFTY = []

targettobuy = ''
targettosell = ''
targettoexit = ''


def initialisedTockenMap():
    url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
    d = requests.get(url).json()
    global token_df
    token_df = pd.DataFrame.from_dict(d)
    token_df['expiry'] = pd.to_datetime(token_df['expiry'])
    token_df = token_df.astype({'strike': float})
    # print('check', token_df)
    placeorderdetails()


def fetchdataandreturn_pivot():
    username = 'YourTradingViewUsername'
    password = 'YourTradingViewPassword'

    tv = TvDatafeed(username, password)
    # index
    BANKNIFTY_index_data = tv.get_hist(symbol='BANKNIFTY', exchange='NSE', interval=Interval.in_daily, n_bars=3)
    data = BANKNIFTY_index_data
    # print(data['high'].values[-2], data['low'].values[-2], data['close'].values[-2])
    high_price = data['high'].values[-2]
    low_price = data['low'].values[-2]
    close_price = data['close'].values[-2]
    datafile = []
    # print(high_price, low_price, close_price)
    # Calculate Fibonacci Levels
    pi = (high_price + low_price + close_price) / 3
    R1 = pi + (0.382 * (high_price - low_price))
    R2 = pi + (0.6182 * (high_price - low_price))
    R3 = R2 + (R2 - R1)
    S1 = pi - (0.382 * (high_price - low_price))
    S2 = pi - (0.6182 * (high_price - low_price))
    S3 = S2 - (R1 - S1)
    fibonacci_levels = {
        'p': round(pi,2),
        's1': round(S1,2),
        'r1': round(R1,2),
        's2': round(S2,2),
        'r2': round(R2,2),
        'r3': round(R3,2),
        's3': round(S3,2)
    }
    global pivot_fibo_level
    pivot_fibo_level = fibonacci_levels



def defineresistancelevel(fibo_level,close):
  data = fibo_level
  filter_value = close

  matching_keys = [key for key, value in data.items() if value >= filter_value]
  max_key = min(matching_keys, key=lambda k: data[k], default='p')
  return max_key

def definesupportlevel(fibo_level,close):
  data = fibo_level
  filter_value = close

  matching_keys = [key for key, value in data.items() if value <= filter_value]
  max_key = max(matching_keys, key=lambda k: data[k], default='p')
  return max_key


def orderplacewithpivot(df,param):
    print(pivot_fibo_level)
    Method_pe = 'ce' if param == 'buy' else 'pe'
    Methor_ce = 'pe' if param == 'sell' else 'ce'
    r_level = defineresistancelevel(pivot_fibo_level,df.close.values[-1])
    s_level = definesupportlevel(pivot_fibo_level,df.close.values[-1])

    print('resistance',r_level,'supports',s_level)

    if r_level in pivot_fibo_level or s_level in pivot_fibo_level:

        if df.high.values[-2] >= pivot_fibo_level[r_level] and df.close.values[-1] < pivot_fibo_level[r_level]:
                return Method_pe
        elif df.low.values[-1] <= pivot_fibo_level[s_level] and df.close.values[-1] > pivot_fibo_level[s_level]:
                return Methor_ce
        else:
              print ("nothing")
    else:
        print ("nothing")


def getTokenInfo(exch_seg,instrumenttype,symbol,strike_price,pe_ce, expiry_day = None):
    df = token_df
    strike_price = strike_price*100
    if exch_seg == 'NSE':
        # print('nse')
        eq_df = df[(df['exch_seg'] == 'NSE')]
        # print(eq_df[(eq_df['name'] == 'BANKNIFTY')],'---####---')
        return eq_df[(eq_df['name'] == 'BANKNIFTY')]
    elif exch_seg == 'NFO' and (instrumenttype == 'OPTSTK' or instrumenttype == 'OPTIDX'):
        print('nfo')
        return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol) & ((df['strike'] == strike_price)) & (df['symbol'].str.endswith(pe_ce)) & (df['expiry'] >= str(datetime.date.today()))].sort_values(by=['expiry'])

def placeorderdetails():
    tokeninfo = getTokenInfo('NSE', 'OPTIDX', 'BANKNIFTY', '', '').iloc[0]['token']
    print(tokeninfo, "---fghjk")
    global LTP
    LTP = obj.ltpData('NSE', 'BANKNIFTY', tokeninfo)['data']['ltp']
    RTM = int(round(LTP / 100) * 100)  # to get check acurate price
    print(LTP, RTM)
    ## now check price and place order details

    global ce_symbol
    global pe_symbol

    ce_symbol = getTokenInfo('NFO', 'OPTIDX', 'BANKNIFTY', RTM, 'CE').iloc[0]
    pe_symbol = getTokenInfo('NFO', 'OPTIDX', 'BANKNIFTY', RTM, 'PE').iloc[0]


def PlaceOredrExit():
    placeOREDR = False

def getorderBook():
    tradebook = obj.position()
    # print(OrderBook)
    #if len(selltradednity) > 0 or len(buy_traded_stock) > 0:
    if tradebook['data'] is not None:
        for a in tradebook['data']:
            if a['symbolname'] == 'NIFTY':
                return False
            else:
                return True
    else:
        return True


def checkorderlimit():
    try:
        getposition = obj.position()
        if getposition['data'].len >= 3:
           placeOREDR = False


    except Exception as e:
        print("error in check number in Position: {}".format(e))
        sendAlert("error in check number in Position: {}".format(e))



def sendAlert(bot_message):
    get_message = format(bot_message)
    print(get_message)

    bot_token = "5707293106:AAEPkxexnIdoUxF5r7hpCRS_6CHINgU4HTw"
    bot_chatid = "2027669179"
    send_message = "https://api.telegram.org/bot" + bot_token + "/sendMessage?chat_id=" + bot_chatid + \
                   "&parse_mode=MarkdownV2&text=" + bot_message

    # response = requests.get(send_message)
    response = requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', data={'chat_id': bot_chatid, 'text': bot_message})

    print(response)
    return response.json()


def GettingLtpData(script, token, order):


    # orderparams = {
    #     "variety": "NORMAL",
    #     "tradingsymbol": script,
    #     "symboltoken": token,
    #     "transactiontype": order,
    #     "exchange": exchange,
    #     "ordertype": "LIMIT",
    #     "producttype": "INTRADAY",,
    #     "duration": "DAY",
    #     "price": ltp,
    #     "squareoff": "0",
    #     "stoploss": "0",
    #     "quantity": quantity
    # }

    # if placeOREDR:
    # orderId = obj.placeOrder(orderparams)
    # print(
    #         f"{order} order Place for {script} at : {datetime.datetime.now()} with Order id {orderId}"
    #     )


    bot_message = f'order status:{order} for {script} with price {token} and the time is {datetime.datetime.now()}'
    sendAlert(bot_message)
def place_order(token, symbol, qty, exch_seg, buy_sell, ordertype, price):
        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol": symbol,
            "symboltoken": token,
            "transactiontype": buy_sell,
            "exchange": exch_seg,
            "ordertype": ordertype,
            "producttype": "INTRADAY",
            "duration": "DAY",
            "squareoff": "0",
            "stoploss": "0",
            "quantity": qty,
            'price': price
        }
        # orderId = obj.placeOrder(orderparams)
        # print(orderId)

        if placeOREDR:
            # orderId = obj.placeOrder(orderparams)
            print(
                    f"{buy_sell} order Place for {symbol} at : {datetime.datetime.now()} with Order id {price}"
                )

        bot_message = f'order status:{buy_sell} for {symbol} with price {token} and the time is {datetime.datetime.now()}'
        sendAlert(bot_message)


def exitQuert():
    api_key = document.api_key
    user_id = document.user_id
    password = document.password
    totp = pyotp.TOTP(document.totp).now()

    try:
        obj = SmartConnect(api_key=api_key)
        token = obj.generateToken(obj.generateSession(user_id, password, totp)["data"]["refreshToken"])
        getposition = obj.position()

        for a in getposition['data']:
            LTP = obj.ltpData(a["exchange"], a["tradingsymbol"], a["symboltoken"])
            getltp = LTP["data"]["ltp"]

            if (a["tradingsymbol"] not in traded_list_exit):

                traded_list_exit.append(a["tradingsymbol"])
                transactionType = "SELL" if int(a['netqty']) > 0 else "BUY"

                orderparams3 = {"variety": "NORMAL", "tradingsymbol": a["tradingsymbol"], "symboltoken": a["symboltoken"],
                                "transactiontype": transactionType, "exchange": a["exchange"], "ordertype": "LIMIT",
                                "producttype": a["producttype"], "duration": "DAY", "price": getltp, "squareoff": "0",
                                "stoploss": "0", "quantity": abs(int(a["netqty"]))}
                orderId3=obj.placeOrder(orderparams3)
                print(f"{orderparams3} order Place for {a['symboltoken']} at : {datetime.datetime.now()} with Order id {orderId3} order id quantity :{a['netqty']} ")

                time.sleep(2)

    except Exception as e:
        print("error: {}".format(e))
        bot_message = f"error when exit {e}"
        sendAlert(bot_message)

def strategy():
    print('check stetergy')
    global obj

    current_date_time = datetime.datetime.now()
    form_date = current_date_time - timedelta(days=10)

    api_key = document.api_key
    user_id = document.user_id
    password = document.password
    totp = pyotp.TOTP(document.totp).now()


    try:
        # obj = SmartConnect(api_key=api_key)
        # token = obj.generateToken(obj.generateSession(user_id, password, totp)["data"]["refreshToken"])
        # jwtToken = token['data']["jwtToken"]
        # refreshToken = token['data']['refreshToken']
        # feedToken = token['data']['feedToken']
        # print(obj)

        tv = TvDatafeed()
        hist_data = tv.get_hist(symbol='BANKNIFTY',exchange='NSE',interval=Interval.in_5_minute,n_bars=50)
        # print(hist_data)
        if not hist_data.empty:
            df = pd.DataFrame(
                hist_data,
                columns=['date', 'open', 'high', 'low', 'close','volume'])

            df["sup"] = ta.supertrend(df['high'], df['low'], df['close'], length=10, multiplier=3)['SUPERT_10_3.0']
            df["ema"] = ta.ema(df["close"], length=200)
            df['stx'] = np.where((df['sup'] > 0.00), np.where((df['close'] > df['sup']), 'up', 'down'), np.NaN)

            if not df.empty:
                print('#------------------------------' ,df.close.values[-5],df.close.values[-4],df.close.values[-3],df.close.values[-2],"----",df.sup.values[-1],'-----------------------#',format(datetime.datetime.now()))

                sup_cl = df.sup.values[-1]
                close_cl = df.close.values[-1]
                # pre close
                sup_pre = df.sup.values[-2]
                close_pre = df.close.values[-2]

                # 3 close
                sup_pre3 = df.sup.values[-3]
                close_pre3 = df.close.values[-3]

                # 4 close
                sup_pre4 = df.sup.values[-4]
                close_pre4 = df.close.values[-4]


                # print('order book',getorderBook())
                if not df.empty:
                    if getorderBook():  # (check if BANKNIFTY order is not placed)
                        if close_pre >= sup_pre and close_cl < sup_cl and ('BANKNIFTY' not in buytradedBANKNIFTY):
                            # GettingLtpData('BANKNIFTY', close_cl, "SELL")
                            place_order(pe_symbol['token'], pe_symbol['symbol'], pe_symbol['lotsize'], 'NFO', 'BUY',
                                        'MARKET', 0)
                            buytradedBANKNIFTY.append('BANKNIFTY')


                        elif close_pre <= sup_pre and close_cl > sup_cl and ('BANKNIFTY' not in buytradedBANKNIFTY):
                            # GettingLtpData('BANKNIFTY', close_cl, "BUY")
                            place_order(ce_symbol['token'], ce_symbol['symbol'], ce_symbol['lotsize'], 'NFO', 'BUY',
                                        'MARKET', 0)
                            buytradedBANKNIFTY.append('BANKNIFTY')

                        # elif close_pre4 <= sup_pre4 and close_pre3 <= sup_pre3 and close_pre <= sup_pre and close_cl < sup_cl and ('BANKNIFTY' not in buytradedBANKNIFTY):
                        #     # GettingLtpData('BANKNIFTY', close_cl, "SELL")
                        #     buytradedBANKNIFTY.append('BANKNIFTY')
                        #     place_order(pe_symbol['token'], pe_symbol['symbol'], pe_symbol['lotsize'], 'NFO', 'BUY',
                        #                 'MARKET', 0)
                        #
                        # elif close_pre4 >= sup_pre4 and close_pre3 >= sup_pre3 and close_pre >= sup_pre and close_cl > sup_cl and ('BANKNIFTY' not in buytradedBANKNIFTY):
                        #     # GettingLtpData('BANKNIFTY', close_cl, "BUY")
                        #     place_order(ce_symbol['token'], ce_symbol['symbol'], ce_symbol['lotsize'], 'NFO', 'BUY',
                        #                 'MARKET', 0)
                        #
                        #     buytradedBANKNIFTY.append('BANKNIFTY')


                        elif close_pre > sup_pre  and orderplacewithpivot(df,'buy') == 'ce'and ('BANKNIFTY' not in buytradedBANKNIFTY):
                            place_order(ce_symbol['token'], ce_symbol['symbol'], ce_symbol['lotsize'], 'NFO', 'BUY',
                                        'MARKET', 0)

                            buytradedBANKNIFTY.append('BANKNIFTY')

                        elif close_pre < sup_pre  and orderplacewithpivot(df,'buy') == 'pe' and ('BANKNIFTY' not in buytradedBANKNIFTY):
                            buytradedBANKNIFTY.append('BANKNIFTY')
                            place_order(pe_symbol['token'], pe_symbol['symbol'], pe_symbol['lotsize'], 'NFO', 'BUY',
                                        'MARKET', 0)

                    else:  # (if BANKNIFTY order is placed, then run exit script with supertrend)
                        if close_pre >= sup_pre and close_cl < sup_cl and ('BANKNIFTY' not in selltradednity):
                            # GettingLtpData('BANKNIFTY', close_cl, "SELL")   # (run exit script)
                            place_order(ce_symbol['token'], ce_symbol['symbol'], ce_symbol['lotsize'], 'NFO', 'SELL',
                                        'MARKET', 0)
                            selltradednity.append('BANKNIFTY')

                        elif close_pre <= sup_pre and close_cl > sup_cl and ('BANKNIFTY' not in selltradednity):
                            # GettingLtpData('BANKNIFTY', close_cl, "BUY")   # (run exit script)
                            place_order(pe_symbol['token'], pe_symbol['symbol'], pe_symbol['lotsize'], 'NFO', 'SELL',
                                        'MARKET', 0)
                            selltradednity.append('BANKNIFTY')
                        elif close_pre >= sup_pre and orderplacewithpivot(df,'sell') == 'ce' and ('BANKNIFTY' not in selltradednity):
                            place_order(ce_symbol['token'], ce_symbol['symbol'], ce_symbol['lotsize'], 'NFO', 'SELL',
                                        'MARKET', 0)

                            buytradedBANKNIFTY.append('BANKNIFTY')
                        elif close_pre <= sup_pre and orderplacewithpivot(df,'sell') == 'pe' and ('BANKNIFTY' not in selltradednity):
                            place_order(pe_symbol['token'], pe_symbol['symbol'], pe_symbol['lotsize'], 'NFO', 'SELL',
                                        'MARKET', 0)

                            buytradedBANKNIFTY.append('BANKNIFTY')

            time.sleep(1)



    except Exception as e:
        print("Script Not Working: {}".format(e),format(datetime.datetime.now()))
        bot_message = f"Historic Api failed {e}"
        # sendAlert(bot_message)
        strategy()

    # try:
    #     logout = obj.terminateSession(user_id)
    #     print("Logout Successfull")
    # except Exception as e:
    #     print("Logout failed: {}".format(e))
    #     bot_message = f"Logout failed {e}"
    #     # sendAlert(bot_message)

# try:
#     api_key = document.api_key
#     user_id = document.user_id
#     password = document.password
#     totp = pyotp.TOTP(document.totp).now()
#
#     obj = SmartConnect(api_key=api_key)
#     token = obj.generateSession(user_id, password, totp)
#     print("--------",obj,token)
#     if obj:
#         strategy()
#
#
# except Exception as e:
#     print("Build Connection Error: {}".format(e), format(datetime.datetime.now()))
initialisedTockenMap()
fetchdataandreturn_pivot()
strategy()
schedule.every(2).minutes.do(strategy)
# schedule.every(5).minutes.do(checkorderlimit)
schedule.every().day.at("15:05").do(exitQuert)
schedule.every().day.at("15:00").do(PlaceOredrExit)




while True:
        # print("start tym , CURRENT TIME:{}".format(datetime.datetime.now()))
        try:
            schedule.run_pending()
            time.sleep(2)
        except Exception as e:
            raise e




# important notes:
# obj.tradeBook()
# obj.orderBook()
# obj.position()
# obj.holding()
