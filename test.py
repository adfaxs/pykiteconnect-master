from kiteconnect import KiteConnect
import time
import os
api_key= "f9rhxy460o4aiysb"
api = KiteConnect(api_key=api_key)

name = "KZZ053.txt"

access_token  = open(r"/Users/crosshair/Downloads/pykiteconnect-master/Login/" + name,'r')
access_token = access_token.read()


data = api.set_access_token(access_token)
os.system('clear')

nifty =  api.ltp("NSE:NIFTY 50").get("NSE:NIFTY 50").get('last_price')
NiftyAtmStrike = 0
if (nifty%50)>= 25:
   NiftyAtmStrike = (nifty - nifty%50+50)
elif (nifty%50)<25:
    NiftyAtmStrike =(nifty - nifty%50)

"https://api.kite.trade/instruments"
import requests
URL ="https://api.kite.trade/instruments"
response = requests.get(URL)
open("instruments.txt", "wb").write(response.content)
file = open("instruments.txt" , 'r').read()
index = 'SENSEX'
print(file.split("\n")[0])
# print(file.split("\n")[1])
from datetime import datetime

def closest_expiry_symbol(data_list):
    today = datetime.now().date()
    closest_symbol = None
    min_difference = float("inf")

    for data in data_list:
        values = data.split(",")
        expiry_date_str = values[5]  # Assuming expiry is the 6th value in the array
        expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
        difference = abs((expiry_date - today).days)

        if difference < min_difference:
            min_difference = difference
            closest_symbol = values[2]  # Assuming tradingsymbol is the 3rd value in the array

    return closest_symbol

# Example usage
data_list = []

for i in file.split("\n"):
    try:
      
        if(len(i.split(','))>2 and i.split(',')[10]=='BFO' and i.split(',')[3][1:-1]==index ):
            data_list.append(i)
            print(i)
        
    except Exception as e :
        print(e)


closest_symbol = closest_expiry_symbol(data_list)
print(f"The symbol with the closest expiry date is {closest_symbol}")
import re

contract_string = "NIFTY2390719250CE"

# Extract year and month using regular expression
match = re.search(r'(\d{2})([A-Z]{3})(\d{2})', contract_string)

if match:
    year = int(match.group(1))  # Assuming the year is in 2-digit format
    month = match.group(2)
    print(f"Year: {year}, Month: {month}")
else:
    print("Pattern not found in the string")
