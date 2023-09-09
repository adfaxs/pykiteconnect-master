import Cred
from Login import loginZerodha

import datetime 


Credentials = Cred.Crosshair
api , kws  = loginZerodha(Credentials) 

import pandas as pd
import numpy as np
import talib 
# Example usage
high =[]
low =[]
close =[]
data = api.historical_data( 738561, "2023-09-08 10:40:00", "2023-09-08 15:30:00", "minute", continuous=False, oi=False)
print(data[len(data)-2]['close'])
for min_data in data:
    close.append(float(min_data['close']))
    high.append(float(min_data['high']))
    low.append(float(min_data['low']))
BUY_FLAG  = False

# price_data = [50.25, 51.50, 52.75, 53.25, 53.50, 52.75, 51.80, 51.10, 52.25, 51.75, 50.50, 51.00, 52.00, 52.50]
rsi = talib.RSI(np.array(close) , 14)

print(rsi)
# for rsi in rsi_values:
#     print(f"{rsi:.2f}")
# Example usage


# # price_data = [50.25, 51.50, 52.75, 53.25, 53.50, 52.75, 51.80, 51.10, 52.25, 51.75, 50.50, 51.00, 52.00, 52.50]
# rsi = calculate_rsi(price_data)
# print(rsi)


# print(api.quote("NSE:"))

