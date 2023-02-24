import requests, time, datetime, sched
import tkinter as tk

tokens = {
    'AGIXBUSD': {
        'low_trigger': 0.35,
        'high_trigger': 0.43,
    },
   }
# Define the interval (in seconds)
interval = 20
api_url = 'https://api.binance.com/api/v3/ticker/price'
last_info = None

def check_data():
    for token in tokens:
        params = {'symbol': token}
        response = requests.get(api_url, params=params)
        data = response.json()
        price = float(data['price'])
        low_trigger = tokens[token]['low_trigger']
        high_trigger = tokens[token]['high_trigger']
        # Get the current date and time
        now = datetime.datetime.now()
        # Format the date and time as a string
        date_string = now.strftime("%Y-%m-%d %H:%M:%S")
        assert low_trigger < high_trigger, f'I think you meant different numbers because low_trigger: {low_trigger} > high_trigger: {high_trigger}'
        info = f"{date_string} The current price of {token} is {price} USDT"
        print(info)
        try:
            global message, last_info, root
            if last_info != info:
                message.config(text=info)
                root.title(price)
                last_info = info
        except UnboundLocalError as e:
            
            print(e,"Can't update Main Window's message because it doesn't exist")
            # Create a label with a message to display
            #message = tk.Label(root, text="Init ,message")
        
        if price > high_trigger or price < low_trigger:
            # Create a poput to indicate trigger is reached
            popup = tk.Tk()
            popup.title(f"{token} alert.")
            # Create a label with a message to display
            message = tk.Label(popup, text=f"{token} has hit {price},\nwhich is outside the non-triggering range of {low_trigger} - {high_trigger}.")
            # Add the label to the root
            message.pack()
            # Start the GUI event loop
            popup.mainloop()
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

root.after(interval, check_data)

# Start the GUI event loop
root.mainloop()
