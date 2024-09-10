import datetime
import json
import re
import sqlite3
from typing import List, Union


conn = sqlite3.connect('database.db')
print(conn)

conn.execute('''CREATE TABLE IF NOT  EXISTS ORDERCONDITION(
        id INTEGER PRIMARY KEY,
        condition TEXT NOT NULL
    )''')

conn.execute('''CREATE TABLE IF NOT  EXISTS intradayorder(
        id INTEGER PRIMARY KEY,
        script TEXT NOT NULL
    )''')

conn.execute('''CREATE TABLE IF NOT  EXISTS supportset(
        id INTEGER PRIMARY KEY,
        timeframe TEXT NOT NULL,
        supportlist TEXT NOT NULL,
        symboltype TEXT NOT NULL
    )''')

conn.execute('''CREATE TABLE IF NOT EXISTS ordertoken(
        id INTEGER PRIMARY KEY,
        symbol TEXT NOT NULL,
        exchange TEXT NOT NULL,
        token TEXT NOT NULL,
        ltp REAL NOT NULL,
        lotsize INTEGER NOT NULL,
        profit REAL NOT NULL
    )''')

conn.execute('''CREATE TABLE IF NOT EXISTS cryptoorderbook(
        id INTEGER PRIMARY KEY,
        symbol TEXT NOT NULL,
        exchange TEXT NOT NULL,
        token TEXT NOT NULL,
        ltp REAL NOT NULL,
        lotsize INTEGER NOT NULL,
        profit REAL NOT NULL
    )''')


# conn.execute('''ALTER TABLE cryptoorderbook ADD COLUMN createddate timestamp''')

def insertdata(data):
    query = 'INSERT INTO ORDERCONDITION(condition) VALUES(?);'
    conn.execute(query,(data,))
    conn.commit()

def inserttokenns(symbol,exchange,token,lotsize,ltp,profit):
    date = datetime.datetime.now()
    query = 'INSERT INTO ordertoken(symbol,exchange,token,lotsize,ltp,profit,createddate) VALUES(?,?,?,?,?,?,?);'
    conn.execute(query,(symbol,exchange,token,lotsize,ltp,profit,date))
    conn.commit()

def insertcryptoorder(symbol,exchange,token,lotsize,ltp,profit):
    date = datetime.datetime.now()
    query = 'INSERT INTO cryptoorderbook(symbol,exchange,token,lotsize,ltp,profit,createddate) VALUES(?,?,?,?,?,?,?);'
    conn.execute(query,(symbol,exchange,token,lotsize,ltp,profit,date))
    conn.commit()

def createupport(time,support,symbol):
    query = 'INSERT INTO supportset(timeframe,supportlist,symboltype) VALUES(?,?,?);'
    conn.execute(query,(time,support,symbol,))
    conn.commit()

def insertscript(data,ordertype):
    query = 'INSERT INTO intradayorder(script,ordertype) VALUES(?,?);'
    conn.execute(query,(data,ordertype,))
    conn.commit()

def updatedata(id,data):
    query = 'UPDATE ORDERCONDITION SET condition = ? WHERE id = ?'
    conn.execute(query,(data,id))
    conn.commit()


def updatesupport(id,data):
    query = 'UPDATE supportset SET supportlist = ? WHERE id = ?'
    conn.execute(query,(data,id))
    conn.commit()

def updateorderplace(id,lotsize,profit):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    query = 'UPDATE ordertoken SET lotsize = ?,profit  = ? WHERE id = ?'
    cursor.execute(query,(lotsize,profit,id))
     # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

def updatecrypto(id,lotsize,profit):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    query = 'UPDATE cryptoorderbook SET lotsize = ?,profit  = ? WHERE id = ?'
    cursor.execute(query,(lotsize,profit,id))
     # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()


#updatedata(1,'2')
def fetchdata():
    fetch = conn.execute('SELECT * FROM ORDERCONDITION')
    data = []
    for row in fetch:
        data.append(row)
        print(data)
    return data

def orderbook():
    fetch = conn.execute('SELECT * FROM intradayorder')
    data = []
    for id,script,ordertype in fetch:
        addvalue = {
            'script':script,
            'ordertype':ordertype
        }
        data.append(addvalue)
    print(data)
    return data

def fetchtokennbook():
    fetch = conn.execute('SELECT * FROM ordertoken')
    data = []
    for id,symbol,exchange,token,lotsize,ltp,profit,createddate in fetch:
        addvalue = {
            'id':id,
            'script':symbol,
            'token':token,
            'lotsize':lotsize,
            'ltp':ltp,
            'profit':profit,
            'createddate':createddate
        }
        data.append(addvalue)
    print(data)
    return data

def fetchtcryptoorderbook():
    fetch = conn.execute('SELECT * FROM cryptoorderbook')
    data = []
    for id,symbol,exchange,token,lotsize,ltp,profit,createddate in fetch:
        addvalue = {
            'id':id,
            'script':symbol,
            'token':token,
            'lotsize':lotsize,
            'ltp':ltp,
            'profit':profit,
            'createddate':createddate
        }
        data.append(addvalue)
    print(data)
    return data


def fetchtokennbook():
    fetch = conn.execute('SELECT * FROM ordertoken')
    data = []
    for id,symbol,exchange,token,lotsize,ltp,profit,createddate in fetch:
        addvalue = {
            'id':id,
            'script':symbol,
            'token':token,
            'lotsize':lotsize,
            'ltp':ltp,
            'profit':profit,
            'createddate':createddate
        }
        data.append(addvalue)
    # print(data)
    return data

def fetchsupport():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    fetch = cursor.execute('SELECT * FROM ordertoken')
    data = []
    for id,symbol,exchange,token,lotsize,ltp,profit,createddate in fetch:
        addvalue = {
            'id':id,
            'script':symbol,
            'token':token,
            'lotsize':lotsize,
            'ltp':ltp,
            'profit':profit,
            'createddate':createddate
        }
        data.append(addvalue)
    # print(data)
    return data


def fetchsupportforweb():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    fetch = conn.execute('SELECT * FROM ordertoken')
    data = []
    for id,symbol,exchange,token,lotsize,ltp,profit,createddate in fetch:
        addvalue = {
            'id':id,
            'script':symbol,
            'token':token,
            'lotsize':lotsize,
            'ltp':ltp,
            'profit':profit,
            'createddate':createddate
        }
        data.append(addvalue)
    print(data)
    return data

def deletedata(delete_id):
    query = 'DELETE FROM ORDERCONDITION WHERE id = ?;'
    conn.execute(query, (delete_id,))
    conn.commit()

def deletesupport(delete_id):
    query = 'DELETE FROM supportset WHERE id = ?;'
    conn.execute(query, (delete_id,))
    conn.commit()

def deletescript(delete_id):
    query = 'DELETE FROM intradayorder WHERE script = ?;'
    conn.execute(query, (delete_id,))
    conn.commit()

def deleteordertoken(delete_id):
    query = 'DELETE FROM ordertoken WHERE id = ?;'
    conn.execute(query, (delete_id,))
    conn.commit()

def deletecrypto(delete_id):
    query = 'DELETE FROM cryptoorderbook WHERE id = ?;'
    conn.execute(query, (delete_id,))
    conn.commit()





def get_data(script):
    query = 'SELECT * FROM intradayorder WHERE script = ?;'
    fetch = conn.execute(query, (script,))
    data = []
    for row in fetch:
        data.append(row)
        print(data)
    return data

#deletescript('NCC-EQ')
#get_data('abc')
#insertscript('RALLIS-EQ','BUY')
#insertscript('abc')
#fetchdata()
# orderbook()
# def deletealldata():
#      fetch = fetchsupport()
#      for item in fetch:
#         deletesupport(item['id'])

#createupport("30min","24832.6 24723.7 23893.7 24999.75 24971.75 25078.3 25030.85 24382.6","NIFTY")
#deletesupport(4)
#deletealldata()
#fetchsupport()
#inserttokenns('nifty','nfo','26000','50','135','49076')
# fetchtokennbook()

# def checkcondition():
#      symbol = 'NIFTY'
#      fetchdata = fetchtokennbook()
#      filteristoken = [item for item in fetchdata if re.match(r'^[A-Za-z]+', item['script']).group() == symbol and item['lotsize'] == 0]
#      print('filter',filteristoken)
#
# checkcondition()

def checkprofit():
    fetch = fetchsupportforweb()
    profit = [item['profit'] for item in fetch]
    total_profit = extract_and_sum_profits(profit)
    print(total_profit)
    return total_profit



def extract_and_sum_profits(data: List[Union[str, float]]) -> float:
    total_profit = 0.0

    # Regular expression to extract profit values from strings
    profit_pattern = re.compile(r'profit\s*-\s*(-?\d+(\.\d+)?)')

    for item in data:
        if isinstance(item, str):
            # Find profit values in the string
            matches = profit_pattern.findall(item)
            for match in matches:
                total_profit += float(match[0])
        elif isinstance(item, (int, float)):
            total_profit += float(item)

    return total_profit


# checkprofit()

# checkprofit# deleteordertoken(41)
# def deletestock():
#      fetch = fetchsupportforweb()
#      for item in fetch:
#          if item['script'] == 'BANKNIFTY04SEP2451400PE':
#              deleteordertoken(item['id'])
# #
# #
# #
# deletestock()
# deleteordertoken(152)

# insertcryptoorder('BTCUSD','nfo','26000','50','135','0')
# fetchtcryptoorderbook()



