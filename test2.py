def extract_expiry_from_code(index, strike, code):
    # Calculate the position of the strike within the code
    strike_position = len(index) + len(str(strike))
    
    # Extract the 3-letter expiry
    expiry = code[len(index)+2:strike_position]
    return expiry

# Example inputs
index = "BANKNIFTY"
strike = 44200
code = "BANKNIFTY2390744200PE"

expiry = extract_expiry_from_code(index, strike, code)
print("Extracted Expiry:", expiry)
