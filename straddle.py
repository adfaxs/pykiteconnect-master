from kiteconnect import KiteConnect
import time
import os
import datetime
import Cred
api_key= Cred.Manjunath['api_key']
api = KiteConnect(api_key=api_key)
import threading
name = Cred.Manjunath['user_id']+".txt"

access_token  = open(r"/Users/crosshair/Downloads/pykiteconnect-master/Login/" + name,'r')
access_token = access_token.read()

print(access_token)
api.set_access_token(access_token)
os.system('clear')
# current_time = datetime.datetime.now()
# formatted_time = current_time.strftime('%Y-%m-%d') +" 9:15:00"
# endDate = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')


global OLDPNL
global CommutativePNL
global CommutativePositionBook
OLDPNL =0
CommutativePNL  = {}
CommutativePositionBook = {}
APIs = []
def LoginAccount(Credentials):
    api = KiteConnect(api_key=Credentials['api_key'])
    name = Credentials['user_id']+".txt"

    access_token  = open(r"/Users/crosshair/Downloads/pykiteconnect-master/Login/" + name,'r')
    access_token = access_token.read()

    api.set_access_token(access_token)
    APIs.append(api) 

LoginAccount(Cred.Manjunath)
LoginAccount(Cred.Riyaaz)
LoginAccount(Cred.Milan)
LoginAccount(Cred.Ankit)
LoginAccount(Cred.AnkitShah)
updatedPrices =[]
def PNLUpdate(api):
    
    PositionBook = {}
    global CommutativePNL
    global CommutativePositionBook
    orders = api.orders()
    # orders.append({'instrument_token':287977733 , 'average_price':5 , 'quantity':1000 ,'transaction_type':'SELL'  , 'status':"COMPLETE"})
    for order in orders:
            if order['status'] == 'COMPLETE':
            
             if order['instrument_token'] not in updatedPrices:
                updatedPrices.append(order['instrument_token'])
             if PositionBook.get(order['instrument_token']) == None:
                    
                    if order['transaction_type'] == 'BUY':
                        new_object = {
                            'PNL':0-((order['average_price'])*  int(order['quantity'])),
                            'Quantity':0 +  int(order['quantity'])}
                        PositionBook[order.get('instrument_token')]= new_object
                    else:
                        new_object = {
                            'PNL':0+((order['average_price'])*  int(order['quantity'])),
                            'Quantity':0 - int(order['quantity'])}
                        PositionBook[order.get('instrument_token')]= new_object
             else :
                    if order['transaction_type'] == 'BUY':
                     PositionBook[order['instrument_token']]['PNL'] =  PositionBook.get(order['instrument_token'])['PNL']-((order['average_price'])*  int(order['quantity']))
                     PositionBook[order['instrument_token']]['Quantity'] = PositionBook.get(order['instrument_token'])['Quantity'] +  int(order['quantity'])
                    else:
                     PositionBook[order['instrument_token']]['PNL'] =  PositionBook.get(order['instrument_token'])['PNL'] + ((order['average_price'])*  int(order['quantity']))
                     PositionBook[order['instrument_token']]['Quantity'] = PositionBook.get(order['instrument_token'])['Quantity'] -  int(order['quantity'])
    # print(PositionBook) 
    PNL = 0
    for Position in PositionBook:
       PNL = PNL + PositionBook.get(Position).get("PNL")     
           
    CommutativePNL[api.profile()['user_id']] =PNL
    # print(CommutativePNL)

    # print(updatedPrices)
    CommutativePositionBook[api.profile()['user_id']] =PositionBook
from kiteconnect import KiteTicker

global last_prices
last_prices = {}

for api in APIs:
    PNLUpdate(api)
# PositionBook[289449477]['Quantity'] = -1000
print(CommutativePNL)
print(CommutativePositionBook)
# for PositionBook in CommutativePositionBook:
#     for Position in CommutativePositionBook.get(PositionBook):
        
for PNL in CommutativePNL:
    OLDPNL = OLDPNL + CommutativePNL.get(PNL)
# CommutativePNL.get(PNL)
    
# print(OLDPNL)
# Initialise
kws = KiteTicker(Cred.Manjunath['api_key'], access_token)
def CalculatePNL():
    

    while True:
        time.sleep(1)
        os.system('clear')
        global OLDPNL
        global CommutativePNL
        global CommutativePositionBook
        # print(OLDPNL)
        
        # try:
        PNL_Object ={}
        for PositionBook in CommutativePositionBook:   
                PNL =CommutativePNL.get(PositionBook)
                for Position in CommutativePositionBook.get(PositionBook):
                    # print(CommutativePositionBook.get(PositionBook).get(Position).get('Quantity'))
                    
                    PNL = PNL + (last_prices.get(Position) * CommutativePositionBook.get(PositionBook).get(Position).get('Quantity'))
                    PNL_Object[PositionBook]= PNL
   
            # print(PNL)
        print(PNL_Object)
        # except Exception as e:
        #     print(e)
threading.Thread(target=CalculatePNL , args=[]).start()





def on_ticks(ws, ticks):
    # Callback to receive ticks.
    global last_prices
    for tick in ticks :
        last_prices[tick['instrument_token']] = tick['last_price']
    
    
def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    print("Websocket is Connected")
    ws.subscribe(updatedPrices)

    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_LTP, updatedPrices)

def on_close(ws, code, reason):
    # On connection close stop the event loop.
    # Reconnection will not happen after executing `ws.stop()`
    print("Websocket is Closed")
    ws.stop()
def on_order_update(ws , update ):
    print('rerun the orderbook file ')
    # PNLUpdate()
    time.sleep(1)

    ws.subscribe(updatedPrices)
    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_LTP, updatedPrices)
# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close
kws.on_order_update = on_order_update

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()

# print(data[time_block].get('open'))
