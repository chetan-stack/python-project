from datetime import datetime
import requests
import pandas as pd
import xlwings as xsw

def getparams(symbol,target,type):
    print('option chain check with price : ',target, 'order type : ',type)
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9,bs;q=0.8'
     }


    session = requests.session()
    request = session.get(url,headers=headers)
    cookies = dict(request.cookies)
    # print(cookies)
    response = session.get(url,headers=headers,cookies=cookies).json()['filtered']['data']
    rawdata = pd.DataFrame(response)
    # print(rawdata)
    docdata = []
    for i in response:
        for j,k in i.items():
            if j=='CE' or j=='PE':
                info = k
                info['instrumenet Type'] = j
                docdata.append(info)
    df = pd.DataFrame(docdata)
        # wb = xsw.Book("angle_excel.xlsx")
        # st = wb.sheets('nifty')
        # st.range('A1').value = df
    target = int(target)
    today_date = datetime.today().date().strftime('%d-%b-%Y')  # Get today's date
    # print(df)
    closest_strike_price = min(df['strikePrice'], key=lambda x: abs(x - target))
    unique_strike_prices = sorted(df['strikePrice'].unique())

    # Find the index of the closest strike price in the unique strike prices list
    closest_index = unique_strike_prices.index(closest_strike_price)

    # Find the strike prices before and after the closest one
    previous_strike_price = unique_strike_prices[closest_index - 1] if closest_index > 0 else None
    next_strike_price = unique_strike_prices[closest_index + 1] if closest_index < len(
        unique_strike_prices) - 1 else None

    print("Closest strike price:", closest_strike_price)
    print("Strike price before:", previous_strike_price)
    print("Strike price after:", next_strike_price)
    setdf = df[(df['strikePrice'] == closest_strike_price)]
    minsetdf = df[(df['strikePrice'] == previous_strike_price)]
    maxset = df[(df['strikePrice'] == next_strike_price)]
    # print(setdf,minsetdf,maxset)
    print('strick price',setdf[setdf['instrumenet Type'] == 'PE']['strikePrice'].values[-1],'---',setdf[setdf['instrumenet Type'] == 'PE']['openInterest'].values[-1], '--', setdf[setdf['instrumenet Type'] == 'PE']['changeinOpenInterest'].values[-1], '----',
      setdf['expiryDate'].values[-1], 'PE', '----', setdf[setdf['instrumenet Type'] == 'CE']['openInterest'].values[-1],
      '--', setdf[setdf['instrumenet Type'] == 'CE']['changeinOpenInterest'].values[-1], '----', setdf['expiryDate'].values[0],
      'CE')

    if type == 'ce' and int(setdf[setdf['instrumenet Type'] == 'PE']['changeinOpenInterest'].values[-1]) > int(setdf[setdf['instrumenet Type'] == 'CE']['changeinOpenInterest'].values[-1]):
         return True
    elif type == 'pe' and int(setdf[setdf['instrumenet Type'] == 'PE']['changeinOpenInterest'].values[-1]) < int(setdf[setdf['instrumenet Type'] == 'CE']['changeinOpenInterest'].values[-1]):
         return True
    else:
         return False


def placeorderwhenconfermation(symbol,target,type):
    print('option chain check with price : ',target, 'order type : ',type)
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9,bs;q=0.8'
     }


    session = requests.session()
    request = session.get(url,headers=headers)
    cookies = dict(request.cookies)
    # print(cookies)
    response = session.get(url,headers=headers,cookies=cookies).json()['filtered']['data']
    rawdata = pd.DataFrame(response)
    # print(rawdata)
    docdata = []
    for i in response:
        for j,k in i.items():
            if j=='CE' or j=='PE':
                info = k
                info['instrumenet Type'] = j
                docdata.append(info)
    df = pd.DataFrame(docdata)
        # wb = xsw.Book("angle_excel.xlsx")
        # st = wb.sheets('nifty')
        # st.range('A1').value = df
    target = int(target)
    today_date = datetime.today().date().strftime('%d-%b-%Y')  # Get today's date
    # print(df)
    closest_strike_price = min(df['strikePrice'], key=lambda x: abs(x - target))
    unique_strike_prices = sorted(df['strikePrice'].unique())

    # Find the index of the closest strike price in the unique strike prices list
    closest_index = unique_strike_prices.index(closest_strike_price)

    # Find the strike prices before and after the closest one
    previous_strike_price = unique_strike_prices[closest_index - 1] if closest_index > 0 else None
    next_strike_price = unique_strike_prices[closest_index + 1] if closest_index < len(
        unique_strike_prices) - 1 else None

    print("Closest strike price:", closest_strike_price)
    print("Strike price before:", previous_strike_price)
    print("Strike price after:", next_strike_price)
    setdf = df[(df['strikePrice'] == closest_strike_price)]
    minsetdf = df[(df['strikePrice'] == previous_strike_price)]
    maxset = df[(df['strikePrice'] == next_strike_price)]
    # print(setdf,minsetdf,maxset)
    print('strick price',setdf[setdf['instrumenet Type'] == 'PE']['strikePrice'].values[-1],'---',setdf[setdf['instrumenet Type'] == 'PE']['openInterest'].values[-1], '--', setdf[setdf['instrumenet Type'] == 'PE']['changeinOpenInterest'].values[-1], '----',
      setdf['expiryDate'].values[-1], 'PE', '----', setdf[setdf['instrumenet Type'] == 'CE']['openInterest'].values[-1],
      '--', setdf[setdf['instrumenet Type'] == 'CE']['changeinOpenInterest'].values[-1], '----', setdf['expiryDate'].values[0],
      'CE')
    print(int(setdf[setdf['instrumenet Type'] == 'PE']['changeinOpenInterest'].values[-1]) , int(setdf[setdf['instrumenet Type'] == 'CE']['changeinOpenInterest'].values[-1]) , int(maxset[maxset['instrumenet Type'] == 'PE']['changeinOpenInterest'].values[-1]) , int(maxset[maxset['instrumenet Type'] == 'CE']['changeinOpenInterest'].values[-1]))
    if int(setdf[setdf['instrumenet Type'] == 'PE']['changeinOpenInterest'].values[-1]) > int(setdf[setdf['instrumenet Type'] == 'CE']['changeinOpenInterest'].values[-1]) and int(maxset[maxset['instrumenet Type'] == 'PE']['changeinOpenInterest'].values[-1]) > int(maxset[maxset['instrumenet Type'] == 'CE']['changeinOpenInterest'].values[-1]):
         return 'ce'
    elif int(setdf[setdf['instrumenet Type'] == 'PE']['changeinOpenInterest'].values[-1]) < int(setdf[setdf['instrumenet Type'] == 'CE']['changeinOpenInterest'].values[-1]) and int(minsetdf[minsetdf['instrumenet Type'] == 'PE']['changeinOpenInterest'].values[-1]) < int(minsetdf[minsetdf['instrumenet Type'] == 'CE']['changeinOpenInterest'].values[-1]):
         return 'pe'
    else:
         return 'no order'


def exitorder(symbol,target,type):
    print('option chain check with price : ',target, 'order type : ',type)
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9,bs;q=0.8'
     }


    session = requests.session()
    request = session.get(url,headers=headers)
    cookies = dict(request.cookies)
    # print(cookies)
    response = session.get(url,headers=headers,cookies=cookies).json()['filtered']['data']
    rawdata = pd.DataFrame(response)
    # print(rawdata)
    docdata = []
    for i in response:
        for j,k in i.items():
            if j=='CE' or j=='PE':
                info = k
                info['instrumenet Type'] = j
                docdata.append(info)
    df = pd.DataFrame(docdata)
        # wb = xsw.Book("angle_excel.xlsx")
        # st = wb.sheets('nifty')
        # st.range('A1').value = df
    target = int(target)
    today_date = datetime.today().date().strftime('%d-%b-%Y')  # Get today's date
    # print(df)
    closest_strike_price = min(df['strikePrice'], key=lambda x: abs(x - target))
    unique_strike_prices = sorted(df['strikePrice'].unique())

    # Find the index of the closest strike price in the unique strike prices list
    closest_index = unique_strike_prices.index(closest_strike_price)

    # Find the strike prices before and after the closest one
    previous_strike_price = unique_strike_prices[closest_index - 1] if closest_index > 0 else None
    next_strike_price = unique_strike_prices[closest_index + 1] if closest_index < len(
        unique_strike_prices) - 1 else None

    # print("Closest strike price:", closest_strike_price)
    # print("Strike price before:", previous_strike_price)
    # print("Strike price after:", next_strike_price)
    setdf = df[(df['strikePrice'] == closest_strike_price)]
    minsetdf = df[(df['strikePrice'] == previous_strike_price)]
    maxset = df[(df['strikePrice'] == next_strike_price)]
    # print(setdf,minsetdf,maxset)
    print('strick price',setdf[setdf['instrumenet Type'] == 'PE']['strikePrice'].values[-1],'---',setdf[setdf['instrumenet Type'] == 'PE']['openInterest'].values[-1], '--', setdf[setdf['instrumenet Type'] == 'PE']['changeinOpenInterest'].values[-1], '----',
      setdf['expiryDate'].values[-1], 'PE', '----', setdf[setdf['instrumenet Type'] == 'CE']['openInterest'].values[-1],
      '--', setdf[setdf['instrumenet Type'] == 'CE']['changeinOpenInterest'].values[-1], '----', setdf['expiryDate'].values[0],
      'CE')

    if type == 'ce' and int(setdf[setdf['instrumenet Type'] == 'PE']['changeinOpenInterest'].values[-1]) > int(setdf[setdf['instrumenet Type'] == 'CE']['changeinOpenInterest'].values[-1]):
         return True
    elif type == 'pe' and int(setdf[setdf['instrumenet Type'] == 'PE']['changeinOpenInterest'].values[-1]) < int(setdf[setdf['instrumenet Type'] == 'CE']['changeinOpenInterest'].values[-1]):
         return True
    else:
         return False



# print(getparams('BANKNIFTY',48153,'ce'))
