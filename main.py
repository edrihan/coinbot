import requests, time, datetime, sched
import tkinter as tk

tokens = {
    'AGIXBUSD': {
        'low_trigger': 0.35,
        'high_trigger': 0.42,
    },
   }
# Define the interval (in seconds)
interval = 30
api_url = 'https://api.binance.com/api/v3/ticker/price'
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
        assert low_trigger < high_trigger, f'I think you meant different numbers because low_trigger: {low_trigger} > high_trigger: {high_trigger}
        print(f"{date_string} The current price of {token} is {price} USDT")
        if price > high_trigger or price < low_trigger:
            # Create a new window
            popup = tk.Tk()
            # Set the title of the window
            popup.title(f"{token} alert.")
            # Create a label with a message to display
            message = tk.Label(popup, text=f"{token} has hit {price},\nwhich is outside the non-triggering range of {low_trigger} - {high_trigger}.")
            # Add the label to the window
            message.pack()
            # Start the GUI event loop
            popup.mainloop()

# Create a scheduler object
scheduler = sched.scheduler(time.time, time.sleep)
# Schedule the function to be executed every 'interval' seconds
def schedule_next_execution():
    scheduler.enter(interval, 1, schedule_next_execution)
    check_data()

# Start the scheduler
schedule_next_execution()
scheduler.run()
