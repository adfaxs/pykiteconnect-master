def ExecuteStrangle (API, Variables , TokensForExecution):
    print(TokensForExecution)
    if Variables['ProductType'] == 'MIS':
        ProductType = API.PRODUCT_MIS
    else:
        ProductType = API.PRODUCT_NRML
    print("Placing Order ")
    StopLoss  = 60
    print(Variables)
    if Variables['Index'] =="SENSEX":
                exchange = API.EXCHANGE_BFO
            
    else: 
                exchange = API.EXCHANGE_NFO
                
    OrderResponse ={
        'CEHedge':[],
        'PEHedge':[],
        'CE':[],
        'PE':[],
        # 'CEStopLoss':[],
        # 'PEStopLoss':[],
       
    }
    
    for Type in OrderResponse:
        if Type == 'CEHedge':
            tradingsymbol = TokensForExecution['CEHedge'].get('tysm')
            transaction_type = API.TRANSACTION_TYPE_BUY
            quantity = Variables['HedgeQuantity']   
            order_type= API.ORDER_TYPE_MARKET
            price=0,
            trigger_price=None,

        elif Type == 'PEHedge':
            tradingsymbol = TokensForExecution['PEHedge'].get('tysm')
            transaction_type = API.TRANSACTION_TYPE_BUY
            quantity = Variables['HedgeQuantity'] 
            order_type= API.ORDER_TYPE_MARKET 
            price=0,
            trigger_price=None,
            
        elif Type == 'CE':
            tradingsymbol = TokensForExecution['CE'].get('tysm')
            transaction_type = API.TRANSACTION_TYPE_SELL
            quantity = Variables['Quantity']
            order_type= API.ORDER_TYPE_MARKET
            price=0,
            trigger_price=None,
            
            
        elif Type == 'PE':
            tradingsymbol = TokensForExecution['PE'].get('tysm')
            transaction_type = API.TRANSACTION_TYPE_SELL
            quantity = Variables['Quantity']
            order_type= API.ORDER_TYPE_MARKET
            price=0,
            trigger_price=None,
            
        # if Type == 'CEStopLoss':
        #     tradingsymbol = TokensForExecution['CE'].get('tysm')
        #     transaction_type = API.TRANSACTION_TYPE_BUY
        #     quantity = Variables['Quantity']   
        #     order_type= API.ORDER_TYPE_SL
        #     price=StopLoss+5,
        #     trigger_price=StopLoss,

        # elif Type == 'PEStopLoss':
        #     tradingsymbol = TokensForExecution['PE'].get('tysm')
        #     transaction_type = API.TRANSACTION_TYPE_BUY
        #     quantity = Variables['Quantity']
        #     order_type= API.ORDER_TYPE_SL
        #     price=StopLoss+5,
        #     trigger_price=StopLoss,




        while (quantity> Variables['MaxQty']):

                        OrderResponse[Type]  = API.place_order(variety=API.VARIETY_REGULAR,
                                            tradingsymbol=tradingsymbol,
                                            exchange=exchange,
                                            transaction_type=transaction_type,
                                            quantity=Variables['MaxQty'],
                                            order_type=order_type,
                                            product=ProductType,
                                            validity=API.VALIDITY_DAY, price= price , trigger_price= trigger_price)

                        quantity= quantity- Variables['MaxQty']

        if (quantity> 0):
                            
                        OrderResponse[Type] =  API.place_order(variety=API.VARIETY_REGULAR,
                                            tradingsymbol=tradingsymbol,
                                            exchange=exchange,
                                            transaction_type=transaction_type,
                                            quantity=quantity,
                                            order_type=order_type,
                                            product=ProductType,
                                            validity=API.VALIDITY_DAY, price= price , trigger_price= trigger_price)
                        
        
    print(OrderResponse)
    
def KillAllPendingOrders(API):
    orderbook = API.get_order_book()
    for order in orderbook:
        if order['status'] == "TRIGGER_PENDING":
            API.cancel_order(order["norenordno"])
            print(order)
            
            
def ExecuteShift(API , Variables ,TokensForExecution , SymbolType , OptionChain  , last_prices ):
    global StopLoss
    if Variables['ProductType'] == 'MIS':
        ProductType = API.PRODUCT_MIS
    else:
        ProductType = API.PRODUCT_NRML
    print("Placing Order ")
    print(Variables)
    if Variables['Index'] =="SENSEX":
                exchange = API.EXCHANGE_BFO
            
    else: 
                exchange = API.EXCHANGE_NFO
                
    OrderResponse ={
        'CloseSell':[],
        'CloseBuy':[],
        'Buy':[],
        'Sell':[],
    }
    if SymbolType == 'CE':
        newStrike = TokensForExecution[SymbolType]['strike'] + Variables['strikeDifference']
        
        newSellSymbol =  (str(Variables["Index"] + "23" + Variables['Expiry'] +  str(newStrike ) + "CE"))
        newHedgeStrike = TokensForExecution[SymbolType+ "Hedge"]['strike'] + Variables['strikeDifference']
        newHedgeSymbol = (str(Variables["Index"] + "23" + Variables['Expiry'] +  str(newHedgeStrike ) + "CE"))
    else :
        newStrike = TokensForExecution[SymbolType]['strike'] - Variables['strikeDifference']
        newSellSymbol =  (str(Variables["Index"] + "23" + Variables['Expiry'] +  str(newStrike ) + "PE"))
        newHedgeStrike = TokensForExecution[SymbolType+ "Hedge"]['strike'] - Variables['strikeDifference']
        newHedgeSymbol = (str(Variables["Index"] + "23" + Variables['Expiry'] +  str(newHedgeStrike ) + "PE"))

    for option in OptionChain :
        if option['tysm'] == newSellSymbol:
            newToken =  option['token']
        if option['tysm'] == newHedgeSymbol:
            newHedgeToken =  option['token']

    print(newStrike , newToken , newSellSymbol , last_prices[int(newToken)]) 
    print(newHedgeStrike , newHedgeToken , newHedgeSymbol , last_prices[int(newHedgeToken) ])
    for Type in OrderResponse:
        
        if Type == "CloseSell":
            tradingsymbol = TokensForExecution[SymbolType].get('tysm')
            transaction_type = API.TRANSACTION_TYPE_BUY
            quantity = int(Variables['Quantity'] )
            order_type= API.ORDER_TYPE_MARKET
            price=0,
            trigger_price=None,
        elif Type == "CloseBuy":
            tradingsymbol = TokensForExecution[SymbolType +"Hedge"].get('tysm')
            transaction_type = API.TRANSACTION_TYPE_SELL
            quantity = int(Variables['HedgeQuantity']) 
            order_type= API.ORDER_TYPE_MARKET
            price=0,
            trigger_price=None,
        elif Type == "Buy":
            tradingsymbol = newHedgeSymbol
            transaction_type = API.TRANSACTION_TYPE_SELL
            quantity = int(Variables['HedgeQuantity'])  
            order_type= API.ORDER_TYPE_MARKET
            price=0,
            trigger_price=None,
        elif Type == "Sell":
            tradingsymbol = newSellSymbol
            transaction_type = API.TRANSACTION_TYPE_SELL
            quantity = int(Variables['Quantity'])
            order_type= API.ORDER_TYPE_MARKET
            price=0,
            trigger_price=None,
            
            
        while (quantity> int( Variables['MaxQty'])):

                        OrderResponse[Type]  = API.place_order(variety=API.VARIETY_REGULAR,
                                            tradingsymbol=tradingsymbol,
                                            exchange=exchange,
                                            transaction_type=transaction_type,
                                            quantity=Variables['MaxQty'],
                                            order_type=order_type,
                                            product=ProductType,
                                            validity=API.VALIDITY_DAY, price= price , trigger_price= trigger_price)

                        quantity= quantity- Variables['MaxQty']

        if (quantity> 0):
                            
                        OrderResponse[Type] =  API.place_order(variety=API.VARIETY_REGULAR,
                                            tradingsymbol=tradingsymbol,
                                            exchange=exchange,
                                            transaction_type=transaction_type,
                                            quantity=quantity,
                                            order_type=order_type,
                                            product=ProductType,
                                            validity=API.VALIDITY_DAY, price= price , trigger_price= trigger_price)
    TokensForExecution['CE'] = {'tsym':newSellSymbol , 'token':newToken , 'ltp' :last_prices[newToken]}        
    TokensForExecution['CEHedge'] = {'tsym':newHedgeSymbol , 'token':newHedgeToken , 'ltp' :last_prices[newHedgeToken]} 
    StopLoss  = last_prices[newHedgeToken] + last_prices[TokensForExecution['PE']['token']]
       
    print(TokensForExecution)
