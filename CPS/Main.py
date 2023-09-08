import sys
sys.path.append(r"/Users/crosshair/Downloads/pykiteconnect-master/")
import threading
import requests
from kiteconnect import KiteConnect , KiteTicker
import time
import os
import datetime
import json
import Cred
from Login import loginZerodha
import datetime
from FindExpiry import findExpiry
from AtmStrike import getAtmStrike , getLTP
from OptionChain import setOptionChain , UpdateTokens
from Websocket import UpdateLtpData
from ClosestPremiumStrike import ClosestPremium
from Execution import ExecuteStrangle , ExecuteShift
from TelegramFunctions import send_to_telegram
from py_vollib.black_scholes.greeks.analytical import delta
from py_vollib.black_scholes.implied_volatility import implied_volatility
global Variables
global OptionChain
global Credentials
global Tokens
global last_prices
global WebsocketIsNotInitialized
global WebsocketIsRunning



Tokens = []
OptionChain = []
last_prices ={}


try:
    #  Login 

    Credentials = Cred.Crosshair
    api , kws  = loginZerodha(Credentials) 


    print('Login Done')

      
    #  Loading Variables
    with open('CPS/Variables.json', 'r') as f:
     Variables = json.load(f)['Variables']
    
    # Generating ltp and Atm Strike
    index_ltp , index_instrument_token =  getLTP(api , Variables['Index'])


    send_to_telegram("Ltp of Index is : " + str(index_ltp) + " " + Variables["Index"])

    
    # Initializing with Index Token so that websocket keeps running
    Tokens.append(index_instrument_token)

    
    AtmStrike = getAtmStrike( index_ltp ,Variables['Index'] )
    send_to_telegram("AtmStrike of Index is : " + str(AtmStrike) + " " + Variables["Index"])

    # Generating Current Expiry to be Traded 

    if  Variables.get('Expiry') == None or Variables['Expiry'] == '' :
        Variables['Expiry'] = (findExpiry(ATMStrike=AtmStrike , index= Variables['Index']))
        
    send_to_telegram("Current Expiry is : " + str(Variables["Expiry"]) )


    #  Threaded Websocket Handler
    WebsocketIsRunning = True
    WebsocketIsNotInitialized = True
    
    # Starting a Thread to update LTP Data using Websocket 
    threading.Thread(target=UpdateLtpData , args=[kws , last_prices , Tokens , WebsocketIsRunning ,WebsocketIsNotInitialized ]).start()
    print(len(last_prices))
    while len(last_prices) ==0:
        print(last_prices)

        print('websocket is pending')
        time.sleep(1)
    
    Tokens = UpdateTokens(Variables , last_prices[Variables['IndexToken']], Tokens  , OptionChain)
    
    while (len(kws.subscribed_tokens )<20 ):
        print('Token Update is Pending')
        time.sleep(1)
    while len(last_prices)<20:
        print(last_prices)

        print('websocket is pending')
        time.sleep(1)

    
    print(OptionChain)
       
    print(last_prices)
    OptionChain = (setOptionChain(OptionChain , Variables , last_prices , Tokens ))
    
    # print(OptionChain)
    
    # IV =  implied_volatility()
    print(OptionChain)

    # TokensForExecution = {}
    # TokensForExecution['CE'] , TokensForExecution['PE'] = ClosestPremium(OptionChain, 20 , 20)
    # TokensForExecution['CEHedge'] , TokensForExecution['PEHedge'] = ClosestPremium(OptionChain, 10 , 10)

    # OrderResponse = ExecuteStrangle(api , Variables,TokensForExecution)
    # StopLoss =int( OrderResponse['CE']['ltp'] + OrderResponse['PE']['ltp'] )
    # sl = -1000
    # currentPNL = 0

    # TrailAtPNL = 2000
    # MoveOf = 500
    # TrailBy = 1000


    # while True:

        
    #     if last_prices[int(OrderResponse['CE']['token'])] > StopLoss :
    #         print('sl is hit')
    #         print('remove all sl orders')

    #         ExecuteShift(api , Variables ,TokensForExecution , "CE" , OptionChain , last_prices )
            
    #     elif last_prices[int(OrderResponse['PE']['token'])] > StopLoss :
    #         print('sl is hit')
    #         print('remove all sl orders')
    #         ExecuteShift(api , Variables ,TokensForExecution , "PE" , OptionChain , last_prices )
    #     if (currentPNL > sl):
        
    #         if ( TrailAtPNL < currentPNL):
    #             TrailAtPNL = TrailAtPNL + MoveOf
    #             sl = sl + TrailBy
    #     else :
    #         WebsocketIsRunning = False
    #         squareofAll()
    #         break
        
except Exception as e:
    e_type, e_object, e_traceback = sys.exc_info()
    
    e_filename = os.path.split(
        e_traceback.tb_frame.f_code.co_filename
    )[1]

    e_message = str(e)

    e_line_number = e_traceback.tb_lineno

    print(e , e_filename, e_message, e_line_number)