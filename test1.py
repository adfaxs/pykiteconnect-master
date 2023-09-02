
from kiteconnect import KiteConnect
import time
import os
import datetime
import math
api_key= "f9rhxy460o4aiysb"
api = KiteConnect(api_key=api_key)

name = "KZZ053.txt"

access_token  = open(r"/Users/crosshair/Downloads/pykiteconnect-master/Login/" + name,'r')
access_token = access_token.read()


data = api.set_access_token(access_token)
os.system('clear')




# current_time = datetime.datetime.now()
# formatted_time = current_time.strftime('%Y-%m-%d') +" 9:15:00"
# endDate = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')
            
# time_block = int((int(10) - (9))*12 + (int(30)- 15)/5)
# ltp  = (api.ltp('NSE:NIFTY 50')).get('NSE:NIFTY 50')
# ltp = (api.historical_data(ltp.get('instrument_token'), formatted_time, endDate, '5minute', continuous=False, oi=False))[time_block].get('open')
           
# print(time_block)

# mod = int(ltp) % 50
# print(ltp)
# if mod < 25:
#                   atmStrike = int(math.floor(ltp/50))*50
# else:
#                   atmStrike = int(math.ceil(ltp/50))*50
# print(atmStrike)