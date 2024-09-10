import datetime
import json
import re
import sqlite3
from typing import List, Union


conn = sqlite3.connect('database.db')
print(conn)





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



def insertcryptoorder(symbol,exchange,token,lotsize,ltp,profit):
    date = datetime.datetime.now()
    query = 'INSERT INTO cryptoorderbook(symbol,exchange,token,lotsize,ltp,profit,createddate) VALUES(?,?,?,?,?,?,?);'
    conn.execute(query,(symbol,exchange,token,lotsize,ltp,profit,date))
    conn.commit()





def updatecrypto(id,lotsize,profit):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    cursor = conn.cursor()
    query = 'UPDATE cryptoorderbook SET lotsize = ?,profit  = ? WHERE id = ?'
    cursor.execute(query,(lotsize,profit,id))
     # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()



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



def deletecrypto(delete_id):
    query = 'DELETE FROM cryptoorderbook WHERE id = ?;'
    conn.execute(query, (delete_id,))
    conn.commit()






# insertcryptoorder('BTCUSD','nfo','26000','50','135','0')
# fetchtcryptoorderbook()



