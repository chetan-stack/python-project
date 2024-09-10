import requests
from datetime import datetime, timedelta
import pandas as pd
import crete_update_table
crpto = {
    "BTCUSD":"BTCUSD",
    "ETHUSD":"ETHUSD",
    "XRPUSD":"XRPUSD",
    "BNBUSD":"BNBUSD",
    "ADAUSD":"ADAUSD",
    "DOGEUSD":"DOGEUSD"
}

timeframe_map = {
    '1m': '1m',
    '5m': '5m',
    '15m': '15m',
    '30m': '30m',
}

def fetch_and_process_data(data,rolling_window, level_diff_threshold):
    try:
        # df = data
        df = pd.DataFrame(
                data,
                columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        # print(df.close.values[-1])
        if df is not None:
            resistancelevel = []
            supportlevel = []
            itemclose = df.close.values[-1]
            # print(itemclose)
            supports = df[df.low == df.low.rolling(rolling_window, center=True).min()].close
            resistances = df[df.high == df.high.rolling(rolling_window, center=True).max()].close
            level = pd.concat([supports, resistances])
            level = level[abs(level.diff()) > level_diff_threshold]
            print('levels',level)
            for a in level:
                if a > itemclose:
                    resistancelevel.append(a)
                else:
                    supportlevel.append(a)

            # Handle empty lists
            if resistancelevel:
                registance_item = max(resistancelevel, key=lambda x: x if x > itemclose else float('-inf'))
            else:
                registance_item = None

            if supportlevel:
                support_item = max(supportlevel, key=lambda x: x if x < itemclose else float('-inf'))
            else:
                support_item = None
            # print(level)
            return True, level
            # return df, level, registance_item, support_item,itemclose
        else:
            return False, 'no'
    except Exception as e:
        print('error', e)


def get_historical_data(symbol,time):
  current_date_time = datetime.now() - timedelta(days=1)
  form_date = current_date_time - timedelta(days=10)
  params = {
  'resolution': time,
  'symbol': symbol,
   'start': int(form_date.timestamp()),
  'end': int(current_date_time.timestamp()),
  'count': 100             # Example candle count parameter
  }

  response = requests.get("https://cdn.india.deltaex.org/v2/history/candles", params=params)
  historical_data = response.json()
  # print(len(historical_data['result']))
  last_candles = historical_data['result'][-100:]
  return last_candles


def stetergytosendalert(script, interwal, data, level, closehigh, closelow):
    df = data
    qty = 10
    print(df,level)
    try:
        cetrue = (closehigh < df.close.values[-1]) if closehigh != '' else True
        petrue = (closelow > df.close.values[-1]) if closelow != '' else True

        for a in level:
            if a > df.low.values[-2] and a < df.close.values[-1] and df.Candle_Color.values[-1] == 1 and cetrue:
                crete_update_table.insertcryptoorder(script,'scrpto',script,qty,df.close.values[-1],'0')
            elif a < df.high.values[-2] and a > df.close.values[-1] and df.Candle_Color.values[-1] == 0 and petrue:
                crete_update_table.insertcryptoorder(script,'scrpto',script,qty,df.close.values[-1],'0')

                print('sell')
    except Exception as e:
            print("error: {}".format(e))




def aggregate_data(df, time_frame):
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(df)

    # Convert 'time' column to datetime
    df['time'] = pd.to_datetime(df['time'], unit='s')

    # Set 'time' column as index
    df.set_index('time', inplace=True)

    # Resample and aggregate
    resampled_df = df.resample(time_frame).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last'
    })

    return resampled_df

def stetergy():
  for item in crpto:
    data1m = get_historical_data(item,'1m')
    for interval,key in timeframe_map.items():
      data = get_historical_data(item,key)
      result, level = fetch_and_process_data(data,10, 10)
      df_5min = aggregate_data(data1m, '5T').tail(10)
      closehigh = df_5min.high.values[-2]
      closelow = df_5min.low.values[-2]
      stetergytosendalert(item, interval, data, level, closehigh, closelow)


stetergy()
