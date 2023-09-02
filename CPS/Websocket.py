



def UpdateLtpData(kws , last_prices , Tokens):
    # Tokens = [65260551]

    import time
    import logging
    from kiteconnect import KiteTicker
    oldTokens = []

    logging.basicConfig(level=logging.DEBUG)

    # Initialise.

    # RELIANCE BSE


    # Callback for tick reception.
    def on_ticks(ws, ticks):
        # if len(ticks) > 0:
        #     logging.info("Current mode: {}".format(ticks[0]["mode"]))
        # print(ticks)
        for tick in ticks :
         last_prices[tick['instrument_token']] = tick['last_price']
    


    # Callback for successful connection.
    def on_connect(ws, response):
        logging.info("Successfully connected. Response: {}".format(response))
        ws.subscribe(Tokens)
        ws.set_mode(ws.MODE_LTP, Tokens)
        logging.info("Subscribe to tokens in Full mode: {}".format(Tokens))


    # Callback when current connection is closed.
    def on_close(ws, code, reason):
        logging.info("Connection closed: {code} - {reason}".format(code=code, reason=reason))


    # Callback when connection closed with error.
    def on_error(ws, code, reason):
        logging.info("Connection error: {code} - {reason}".format(code=code, reason=reason))


    # Callback when reconnect is on progress
    def on_reconnect(ws, attempts_count):
   
        logging.info("Reconnecting: {}".format(attempts_count))


    # Callback when all reconnect failed (exhausted max retries)
    def on_noreconnect(ws):
        logging.info("Reconnect failed.")


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
        # count += 1
        # if count % 2 == 0:
        #     if kws.is_connected():
        #         logging.info("### Set mode to LTP for all tokens")
        #         kws.set_mode(kws.MODE_LTP, Tokens)
        # else:
        #     if kws.is_connected():
        #         logging.info("### Set mode to quote for all tokens")
        #         kws.set_mode(kws.MODE_QUOTE, Tokens)
        # on_ticks()
        # print(count)
        # if Tokens 
        if str(Tokens) != str(oldTokens):
            print("hogaya update")
            # kws.unsubscribe(oldTokens)
            oldTokens = list(Tokens)
            kws.subscribe(Tokens)
            
        
        # print(kws.subscribed_tokens)
                
        time.sleep(1)
        # time.sleep(1)
        