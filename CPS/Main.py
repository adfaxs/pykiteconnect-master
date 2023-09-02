import sys
sys.path.append(r"/Users/crosshair/Downloads/pykiteconnect-master/")
import threading
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import time
import os
import datetime
import Cred
from Login import loginZerodha
import datetime
from FindExpiry import findExpiry
from AtmStrike import getAtmStrike
from OptionChain import setOptionChain
from OptionChain import UpdateTokens
from Websocket import UpdateLtpData
from ClosestPremiumStrike import ClosestPremium
from Execution import ExecuteStrangle
from Execution import ExecuteShift
global Variables
global OptionChain
global Credentials
global Tokens

# Login
Credentials = Cred.Crosshair
api  = loginZerodha(Credentials)

access_token  = open(r"/Users/crosshair/Downloads/pykiteconnect-master/Login/" + Credentials['user_id']+'.txt','r')
access_token = access_token.read()
kws = KiteTicker(Credentials['api_key'], access_token)

print('Login Done')

Variables = {
    'Index' :"FINNIFTY",
    'IndexToken':257801,
    'strikeDifference':50,
    'Expiry':'',
    'AtmStrike':'',
    'Quantity':'150',            
    'HedgeQuantity':'200',   
    'MaxQty':'1800',   
    'ProductType':'NRML',   
}         


OptionChain = []
index_=  ((api.ltp('NSE:NIFTY FIN SERVICE')).get('NSE:NIFTY FIN SERVICE'))
print(index_)
AtmStrike = getAtmStrike( index_['last_price'] ,Variables['Index'] )
print(AtmStrike)
if  Variables.get('Expiry') == None or Variables['Expiry'] == '' :
    Variables['Expiry'] = (findExpiry(ATMStrike=AtmStrike , index= Variables['Index']))
    
    

print(Variables['Expiry'])

Tokens = []
global last_prices
last_prices ={}
Tokens.append( index_['instrument_token'])
# Tokens.append(65260551)
threading.Thread(target=UpdateLtpData , args=[kws , last_prices , Tokens]).start()
time.sleep(8)
Tokens = UpdateTokens(Variables , last_prices[Variables['IndexToken']], Tokens  , OptionChain)
time.sleep(5)
print(last_prices)
OptionChain = (setOptionChain(OptionChain , Variables , last_prices , Tokens ))

# global OLDPNL
# global CommutativePNL
# global CommutativePositionBook
# OLDPNL =0
# CommutativePNL  = {}
# CommutativePositionBook = {}
# last_prices = {}

# for api in APIs:
#     PNLUpdate(api)

# updatedPrices =[]
# threading.Thread(target=CalculatePNL , args=[]).start()
# threading.Thread(target=UpdatePNLData , args=[]).start()

TokensForExecution = {}
TokensForExecution['CE'] , TokensForExecution['PE'] = ClosestPremium(OptionChain, 20 , 20)
TokensForExecution['CEHedge'] , TokensForExecution['PEHedge'] = ClosestPremium(OptionChain, 10 , 10)

OrderResponse = ExecuteStrangle(api , Variables,TokensForExecution)
StopLoss =int( OrderResponse['CE']['ltp'] + OrderResponse['PE']['ltp'] )
while True:

    
    if last_prices[int(OrderResponse['CE']['token'])] > StopLoss :
        print('sl is hit')
        print('remove all sl orders')

        ExecuteShift(api , Variables ,TokensForExecution , "CE" , OptionChain , last_prices )
        
    elif last_prices[int(OrderResponse['PE']['token'])] > StopLoss :
        print('sl is hit')
        print('remove all sl orders')
        ExecuteShift(api , Variables ,TokensForExecution , "PE" , OptionChain , last_prices )


  
