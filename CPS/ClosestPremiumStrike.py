def FindClosestPremium(premiums , premium ):
    min = premiums[0]

    diff = abs(premium - premiums[0].get('ltp'))

    for i in premiums:
        if (diff >abs(premium -i.get('ltp'))   ):
            diff = abs( premium -i.get('ltp'))
            min = i
        elif (diff == abs(premium -i.get('ltp')) and i.get('ltp') > min.get('ltp') ):
            diff = abs(premium -i.get('ltp'))
            min = i
    return min


def ClosestPremium(OptionChain , CE_closest , PE_closest):
    PremiumsCE = []
    PremiumsPE = []
    for Option in OptionChain:
        if "CE" in Option['tysm']:
            PremiumsCE.append(Option)
        if "PE" in Option['tysm']:
            PremiumsPE.append(Option)
    CE = FindClosestPremium(PremiumsCE ,CE_closest )
    PE = FindClosestPremium(PremiumsPE ,PE_closest )
    
    # print(CE['token']  , CE['ltp'] , CE['tysm'])
    # print(PE['token']  , PE['ltp'],PE['tysm'])
    return CE , PE