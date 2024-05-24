import json
import sqlite3

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

#conn.execute('''ALTER TABLE intradayorder ADD COLUMN ordertype TEXT''')

def insertdata(data):
    query = 'INSERT INTO ORDERCONDITION(condition) VALUES(?);'
    conn.execute(query,(data,))
    conn.commit()

def insertscript(data,ordertype):
    query = 'INSERT INTO intradayorder(script,ordertype) VALUES(?,?);'
    conn.execute(query,(data,ordertype,))
    conn.commit()

def updatedata(id,data):
    query = 'UPDATE ORDERCONDITION SET condition = ? WHERE id = ?'
    conn.execute(query,(data,id))
    conn.commit()

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

def deletedata(delete_id):
    query = 'DELETE FROM ORDERCONDITION WHERE id = ?;'
    conn.execute(query, (delete_id,))
    conn.commit()

def deletescript(delete_id):
    query = 'DELETE FROM intradayorder WHERE script = ?;'
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
orderbook()


