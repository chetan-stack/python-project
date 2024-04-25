import requests
import pandas as pd
import xlwings as xsw

def getparams(symbol):
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9,bs;q=0.8'
     }

    session = requests.session()
    request = session.get(url,headers=headers)
    cookies = dict(request.cookies)
    print(cookies)
    response = session.get(url,headers=headers,cookies=cookies).json()['records']['data']
    # rawdata = pd.DataFrame(response)
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
    print(df['strikePrice'],df['instrumenet Type'],'dasta')



getparams('NIFTY')
