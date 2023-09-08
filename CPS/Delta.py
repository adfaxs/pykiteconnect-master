
from NorenRestApiPy.NorenApi import NorenApi
from kiteconnect import KiteConnect , KiteTicker
import os
import threading
import json
from datetime import datetime , timedelta
import Cred
import math
import time
from OptionChain import UpdateTokens
from AtmStrike import getAtmStrike ,getLTP
from FindExpiry import findExpiry
from py_vollib.black_scholes.greeks.analytical import delta
from py_vollib.black_scholes.implied_volatility import implied_volatility


import FindExpiry

import requests
URL ="https://api.kite.trade/instruments"
response = requests.get(URL)
open("instruments.txt", "wb").write(response.content)

def GetDateDifferenceInYears():
    

# Define two datetime objects
    date1 = datetime.now()
    date2 = datetime(2023, 9, 14, 3, 30)

    # Calculate the difference in years
    year_difference =( date2 - date1)/ timedelta(days=1)/365

    # Check if we need to subtract 1 year if the second date hasn't reached the same month and day
    

    # print(f"The difference in years is {year_difference} years.")
    return year_difference

   

def ZerodhaApi(Credentials):
    file = open("Login/"+Credentials["user_id"] + '.txt', 'r')

    Credentials['access_token'] = file.read()
    api = KiteConnect(api_key=Credentials["api_key"])
    api.set_access_token(Credentials["access_token"])
    kws = KiteTicker(Credentials['api_key'], Credentials['access_token'])

    return api  , kws


api , kws = ZerodhaApi(Cred.Crosshair)
print(api.profile())


# Get the current date
current_date = datetime.now()

# Calculate the date 7 days ago
seven_days_ago = current_date - timedelta(days=7)

# Format the date as dd-mm-yyyy

# Format the current date as "dd-mm-yyyy"
# formatted_date = current_date.strftime("%d-%m-%Y")
print(seven_days_ago)
to_date = current_date.strftime('%Y-%m-%d') + " 15:30:00"

from_date = seven_days_ago.strftime('%Y-%m-%d') + " 9:15:00"
print(from_date)
print(from_date  , to_date)

Variables ={
    "Index":"NIFTY",
    "IndexToken":256265,
    'strikeDifference':50
}
last_ticks ={} 
Tokens =[]
OptionChain=[]
oldTokens = []
last_prices={}
data ={}
index_ltp , index_instrument_token =  getLTP(api , Variables['Index'])



    
    # Initializing with Index Token so that websocket keeps running
Tokens.append(Variables['IndexToken'])

    
AtmStrike = getAtmStrike( index_ltp ,Variables['Index'] )
# 
    # Generating Current Expiry to be Traded 

if  Variables.get('Expiry') == None or Variables['Expiry'] == '' :
        Variables['Expiry'] = (findExpiry(ATMStrike=AtmStrike , index= Variables['Index']))
        


    #  Threaded Websocket Handler
WebsocketIsRunning = True
    
    # Starting a Thread to update LTP Data using Websocket 


print(Tokens)
    


    # Initialise.

    # RELIANCE BSE

    # Callback for tick reception.
def on_ticks(ws, ticks):
        # if len(ticks) > 0:
        #     logging.info("Current mode: {}".format(ticks[0]["mode"]))
        # print(ticks)
        for tick in ticks :
         last_prices[tick['instrument_token']] = tick['last_price']
        # print(ticks)
        
         
        
    


    # Callback for successful connection.
def on_connect(ws, response):
        ws.subscribe(Tokens)
        ws.set_mode(ws.MODE_LTP, Tokens)


    # Callback when current connection is closed.


    # Assign the callbacks.
kws.on_ticks = on_ticks

kws.on_connect = on_connect

    # Infinite loop on the main thread.
    # You have to use the pre-defined callbacks to manage subscriptions.
kws.connect(threaded=True)

    # Block main thread

count = 0
time.sleep(1)
while WebsocketIsRunning:
    try:
     if AtmStrike != getAtmStrike( last_prices[Variables['IndexToken']] ,Variables['Index'] ):
            oldTokens = list(Tokens)
            kws.subscribe(Tokens)
            Tokens = UpdateTokens(Variables , last_prices[Variables['IndexToken']], Tokens  , OptionChain) 
    except:
        print("AtmStrike Not Ready")
    
    if str(Tokens) != str(oldTokens):
            # kws.unsubscribe(oldTokens)
            oldTokens = list(Tokens)
            kws.subscribe(Tokens)
            Tokens = UpdateTokens(Variables , last_prices[Variables['IndexToken']], Tokens  , OptionChain)
        # print(kws.subscribed_tokens)
    try:
        for Option in OptionChain :
            Option['ltp']= last_prices[int(Option['token'])]
            if ("CE" in Option['tysm'] ):
                Flag = 'c'
            else: Flag ='p'
            Option['iv'] = implied_volatility(price=Option['ltp'] , S=last_prices[Variables['IndexToken']]  ,K = AtmStrike,t = GetDateDifferenceInYears() ,  r = 0.1 , flag= Flag)
            print(Option['iv'])
            Option['delta'] = delta( S=last_prices[Variables['IndexToken']]  ,K = AtmStrike,t = GetDateDifferenceInYears() ,  r = 0.1 , flag= Flag , sigma= Option['iv'])

        # data[datetime.now()]= OptionChain 
        print(OptionChain)  
        
        time.sleep(2000)
        # print(data) 
    except Exception as e:
        print("Chain Not Ready" ,e)     
    time.sleep(1)
        # time.sleep(1)
        