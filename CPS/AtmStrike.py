import os 
import math
import time
def getAtmStrike (ltp , index):
    try:
      atmStrike =0
      if(index =="BANKNIFTY"):
            # ltp = (api.ltp('NSE:NIFTY BANK')).get('NSE:NIFTY BANK').get('last_price')
            mod = int(ltp) % 100
            if mod < 50:
                  atmStrike = int(math.floor(ltp/100))*100
            else:
                  atmStrike = int(math.ceil(ltp/100))*100

      elif(index =="NIFTY"):   
            # ltp = ltp = (api.ltp('NSE:NIFTY 50')).get('NSE:NIFTY 50').get('last_price')

            mod = int(ltp) % 50
            if mod < 25:
                  atmStrike = int(math.floor(ltp/50))*50
            else:
                  atmStrike = int(math.ceil(ltp/50))*50

      elif(index =="FINNIFTY"):   
            # ltp = (api.ltp('NSE:NIFTY FIN SERVICE')).get('NSE:NIFTY FIN SERVICE').get('last_price')

            mod = int(ltp) % 50
            if mod < 25:
                  atmStrike = int(math.floor(ltp/50))*50
            else:
                  atmStrike = int(math.ceil(ltp/50))*50
      elif(index =="SENSEX"):   
            # ltp = (api.ltp('BSE:SENSEX')).get('BSE:SENSEX').get('last_price')

            mod = int(ltp) % 100
            if mod < 50:
                  atmStrike = int(math.floor(ltp/100))*100
            else:
                  atmStrike = int(math.ceil(ltp/100))*100
      
      elif(index =="MIDCPNIFTY"):   
            # ltp = (api.ltp('NSE:NIFTY MID SELECT')).get('NSE:NIFTY MID SELECT').get('last_price')

            mod = int(ltp) % 25
            if mod < 12.5:
                  atmStrike = int(math.floor(ltp/25))*25
            else:
                  atmStrike = int(math.ceil(ltp/25))*25
      
      return atmStrike
    except Exception as e :
        while True:
         os.system('clear')  
         print(e)
         time.sleep(10000)
         
def getLTP(api , index):
      print("Inside")
      try:
            if(index =="BANKNIFTY"):
                  ltp = (api.ltp('NSE:NIFTY BANK')).get('NSE:NIFTY BANK')
                

            elif(index =="NIFTY"):   
                  ltp = ltp = (api.ltp('NSE:NIFTY 50')).get('NSE:NIFTY 50')

            elif(index =="FINNIFTY"):   
                  ltp = (api.ltp('NSE:NIFTY FIN SERVICE')).get('NSE:NIFTY FIN SERVICE')

            elif(index =="SENSEX"):   
                  ltp = (api.ltp('BSE:SENSEX')).get('BSE:SENSEX')

            
            elif(index =="MIDCPNIFTY"):   
                  ltp = (api.ltp('NSE:NIFTY MID SELECT')).get('NSE:NIFTY MID SELECT')

            print(ltp)

            return ltp['last_price'] , ltp['instrument_token']
      except Exception as e :
        while True:
         os.system('clear')  
         print(e)
         time.sleep(10000)
      