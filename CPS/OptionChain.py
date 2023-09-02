
from AtmStrike import getAtmStrike
import time 
def setOptionChain (OptionChain , Variables , last_prices  , Tokens):
    
    LTP = last_prices[Variables['IndexToken']]
    AtmStrike = getAtmStrike(LTP , Variables['Index'])
    if OptionChain  == [] or str(AtmStrike) != (Variables['AtmStrike']):
     Tokens = UpdateTokens(Variables , LTP , Tokens  , OptionChain)
     for Option in  OptionChain: 
            Option['ltp']=last_prices[int(Option['token'])]

     Variables['AtmStrike'] = str(AtmStrike)
    else:

        for Option in  OptionChain: 
            Option['ltp']=last_prices[int(Option['token'])]
            
        Variables['AtmStrike'] = str(AtmStrike)
        
 
    # return OptionChain
    return OptionChain 

def UpdateTokens(Variables , LTP  , Tokens  , OptionChain  ):
    # global Tokens
    file = open("instruments.txt" , 'r').read()

    AtmStrike = getAtmStrike(LTP , Variables['Index'])
    Scripts = []
    count =  -10
    while count <= 10 :
     Scripts.append(str(Variables["Index"] + "23" + Variables['Expiry'] +  str(AtmStrike + (count * Variables['strikeDifference'])) + "CE"))
     Scripts.append(str(Variables["Index"] + "23" + Variables['Expiry'] +  str(AtmStrike + (count * Variables['strikeDifference'])) + "PE"))
     count = count +1 
    # print(Scripts)
    
   
    from datetime import datetime

    # Example usage
    data_list = []

    for i in file.split("\n"):
        try:
            i = i.split(',')
            # if(len(i.split(','))>5  and i.split(',')[2]==Script ):
            if i[2] in Scripts: 
                # print(i)
                # data_list.append(i)
                # print(i)
                OptionChain.append({'tysm':i[2] , 'token':i[0] , 'strike':int(i[6])})
                Tokens.append(int(i[0]))
                # print(i)
            
        except Exception as e :
            print()
            # print(e)
    
    return Tokens