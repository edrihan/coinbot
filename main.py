import requests, time, datetime, sched
from pprint import pprint

import tkinter as tk
from dotenv import dotenv_values # pip install python-dotenv

config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
print(config)
# define the API endpoint for getting exchange info
url = 'https://api.binance.com/api/v3/exchangeInfo'

# make the API request and get the response
response = requests.get(url)

# parse the response JSON and extract the token symbols
data = response.json()
symbols = data['symbols']
valid_tokens_binance = set()
for symbol in symbols:
    base_asset = symbol['baseAsset']
    quote_asset = symbol['quoteAsset']
    valid_tokens_binance.add(base_asset)
    valid_tokens_binance.add(quote_asset)
valid_tokens_binance = list(valid_tokens_binance)
valid_tokens_binance.sort()
print('\n'.join(valid_tokens_binance))


tokens = {
    'AGIXBUSD': {
        'low_trigger': 0.35,
        'high_trigger': 0.45,
    },
    'ADABUSD':{
    },
    'BTCBUSD':{},
    
   }
# Define the interval (in seconds)
interval = 2
interval *= 1000
api_url = 'https://api.binance.com/api/v3/ticker/price'
last_info = None

def update_gui():
    global tokens
    message.config(text=info)
    root.title(tokens[list(tokens.keys())[0]]['price_binance'])

def check_data():
    global message, last_info, root, info, price
    # Get the current date and time
    now = datetime.datetime.now()
    # Format the date and time as a string
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")
    for token in tokens:
        params = {'symbol': token}
        response = requests.get(api_url, params=params)
        data = response.json()
        try:
            price_binance = float(data['price'])
        except KeyError as e:
            print( '\n'+  f"{token} not found by binance API")
            raise e
        tokens[token]['price_binance'] = price_binance
        if 'low_trigger' in tokens[token].keys(): 
            low_trigger = tokens[token]['low_trigger']
        if 'high_trigger' in tokens[token].keys():
            high_trigger = tokens[token]['high_trigger']
        
        if all([k in tokens[token].keys() for k in ('low_trigger','high_trigger')]):
            assert low_trigger < high_trigger, f'I think you meant different numbers because low_trigger: {low_trigger} > high_trigger: {high_trigger}'
        
        if ('high_trigger' in tokens[token].keys() and (price_binance > high_trigger)) or ('low_trigger' in tokens[token].keys() and (price_binance < low_trigger)):
            
            # Create a popup to indicate trigger is reached
            popup = tk.Tk()
            popup.title(f"{token} alert.")
            # Create a label with a message to display
            message = tk.Label(popup, text=f"{token} has hit {price_binance},\nwhich is outside the non-triggering range of {low_trigger} - {high_trigger}.")
            # Add the label to the root
            message.pack()
            # Start the GUI event loop
            popup.mainloop()
    
    info = f"Last updated {date_string}"
    for token in tokens.keys():
        info += f"\n{token} is {tokens[token]['price_binance']} USDT"

    try:
        if last_info != info:
            root.after(1,update_gui)
            last_info = info
    except UnboundLocalError as e:
        print(e,"Can't update Main Window's message because it doesn't exist")
        
    root.after(interval, check_data)

# Create a root window
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# Create the Tkinter root and set its initial resolution
root.geometry("400x300")
root.title("Main Window")
# Create a label with a message to display
message = tk.Label(root, text="Info about shit\nAnd...")
# Add the label to the root
message.pack()

#root.after(interval, check_data)
check_data()
update_gui()

# Start the GUI event loop
root.mainloop()
