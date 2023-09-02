
import time 
import os 
from kiteconnect import KiteConnect


def loginZerodha(Credentials):
    # try:
        api_key= Credentials['api_key']
        api = KiteConnect(api_key=api_key)
        name = Credentials['user_id']+".txt"

        access_token  = open(r"/Users/crosshair/Downloads/pykiteconnect-master/Login/" + name,'r')
        access_token = access_token.read()

    
        api.set_access_token(access_token)
        return api 
    # except Exception as e :
    #     while True:
    #      os.system('clear')  
    #      print(e)
    #      time.sleep(10000)
         
    
