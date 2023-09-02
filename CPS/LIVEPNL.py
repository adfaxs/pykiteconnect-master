import time

import sys
sys.path.append(r"/Users/crosshair/Downloads/pykiteconnect-master/CPS/")
import os
import datetime

import threading
import requests


def send_to_telegram(message):

    apiToken = '6058041177:AAHhrqXPDRa1vghxQu_dTyTXTar1JRgNjCo'
    chatID = '1083941928'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)


def PNLUpdate(api):
    
    PositionBook = {}
    global CommutativePNL
    global CommutativePositionBook
    orders = api.orders()
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
    print(PositionBook)
    PNL = 0
    for Position in PositionBook:
       PNL = PNL + PositionBook.get(Position).get("PNL")     
           
    CommutativePNL[api.profile()['user_id']] =PNL
  
    CommutativePositionBook[api.profile()['user_id']] =PositionBook





def CalculatePNL():

    while True:
        os.system('clear')
        global OLDPNL
        
        global CommutativePNL
        global CommutativePositionBook
        # print(OLDPNL)
       
        try:
         PNL_Object ={}
         for PositionBook in CommutativePositionBook:   
                PNL =CommutativePNL.get(PositionBook)
                for Position in CommutativePositionBook.get(PositionBook):
                    # print(CommutativePositionBook.get(PositionBook).get(Position).get('Quantity'))
                    
                    PNL = PNL + (last_prices.get(Position) * CommutativePositionBook.get(PositionBook).get(Position).get('Quantity'))
                    PNL_Object[PositionBook]= round(PNL,0)
   
            # print(PNL)
         print(PNL_Object)
         send_to_telegram(str(PNL_Object))
        

        except Exception as e:
            print(e)
        time.sleep(1)









def UpdatePNLData(kws , last_prices , Tokens):
    # Tokens = [65260551]

    import time
    import logging
    from kiteconnect import KiteTicker
    # oldTokens = []
    def on_ticks(ws, ticks):
        # Callback to receive ticks.
        global last_prices
        for tick in ticks :
            last_prices[tick['instrument_token']] = tick['last_price']
        
        
    def on_connect(ws, response):
        print("Websocket is Connected")
        ws.subscribe(updatedPrices)

        ws.set_mode(ws.MODE_LTP, updatedPrices)


    def on_order_update(ws , update ):
        global OLDPNL
        OLDPNL = 0
        print('rerun the orderbook file ')
        PNLUpdate()
        for PNL in CommutativePNL:
            OLDPNL = OLDPNL + CommutativePNL.get(PNL)


        time.sleep(1)

        ws.subscribe(updatedPrices)
        ws.set_mode(ws.MODE_LTP, updatedPrices)



 

    # Assign the callbacks.
    kws.on_ticks = on_ticks
    kws.on_close = on_close
    kws.on_error = on_error
    kws.on_connect = on_connect
    kws.on_reconnect = on_reconnect
    kws.on_noreconnect = on_noreconnect

    # Infinite loop on the main thread.
    # You have to use the pre-defined callbacks to manage subscriptions.
    kws.connect(threaded=True)

    # Block main thread

    count = 0
    time.sleep(2)
    while True:
       
        # if str(Tokens) != str(oldTokens):
        #     print("hogaya update")
        #     # kws.unsubscribe(oldTokens)
        #     oldTokens = list(Tokens)
        #     kws.subscribe(Tokens)
        
        
                
        time.sleep(1)
        # time.sleep(1)
        
   



