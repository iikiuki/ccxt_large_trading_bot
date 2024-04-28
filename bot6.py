import ccxt
import time
import math
import dontshareconfig 

# Configuration
SYMBOL = 'ENA/USDT'
symbol_2= 'ENA'
# Adjust the BTC amount to buy


# Initialize the Phemex exchange with your credentials
exchange = ccxt.phemex({
    'apiKey': dontshareconfig.id,
    'secret': dontshareconfig.secret,
    'enableRateLimit': True,
})
stoptime=60


# Function to fetch the current price for the specified symbol
def fetch_price(symbol):
    try:
        ticker = exchange.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        print("Error fetching price:", e)
        return None
# coin_price = fetch_price(SYMBOL)
AMOUNT_TO_BUY =((exchange.fetch_free_balance()['USDT'])-0.5*(exchange.fetch_free_balance()['USDT']))/fetch_price(SYMBOL)


# AMOUNT_TO_BUY = 1/coin_price


# Function to place a market order to buy or sell

def place_market_order(symbol, side, amount):
    try:
        order = exchange.create_order(symbol, 'market', side, amount)
        print(f"Market order placed: {side} {amount} of {symbol}")
        return order
    except Exception as e:
        print("Error placing order:", e)
        return None


def place_market_sell_order(symbol,amount):
    try:
        order = exchange.create_market_sell_order(symbol,amount)
        print(f"Market order placed: \"\"sell\"\" :{amount} of {symbol}")
        return order
    except Exception as e:
        print("Error placing order:", e)
        return None

# Simple trading bot that buys and then sells if the price drops by 0.01%

while True :

    if exchange.fetch_free_balance()['USDT']<2.11:
        break

    def trading_bot():
        global stoptime
        # Buy at the current market price
        initial_price = fetch_price(SYMBOL)

        if initial_price is None:
            print("Failed to fetch initial price.")
            return

        print(f"Initial price: {initial_price}")

        # Place a buy order
        place_market_order(SYMBOL, 'buy', AMOUNT_TO_BUY)

        # Monitor the price in a loop
        price_list = []
        while True:
            # current_price = fetch_price(SYMBOL)
            current_price = exchange.fetch_order_book(SYMBOL)['bids'][0][0]
            print(f"now_price  :{current_price}")
            if stoptime > 30:
                stoptime-=1

            if current_price is not None:
                # Calculate the price drop as a percentage
                # price_drop = (initial_price - current_price) / initial_price
                


                print(f"initial_price: {initial_price}")
                price_list.append(current_price)
                print(f"max num    :{max(price_list)}")
                sell_price_maby = max(price_list)-(0.001*max(price_list))
                print(f"sell price :{sell_price_maby} \n")
                # print(exchange.fetch_free_balance())

                # print(f"{initial_price}\n")
                # if price_drop >= PRICE_DROP_THRESHOLD:
                if current_price < max(price_list)-(0.015*max(price_list))  : # or current_price < initial_price:   #+(initial_price*0.001)  :
                    # Sell if the price has dropped by 0.01% or more
                    print(f"Price drop detected, \"\"selling...\"\"")
                    # place_market_order(SYMBOL, 'sell', int(AMOUNT_TO_BUY))
                    place_market_sell_order(SYMBOL,(exchange.fetch_free_balance()[symbol_2])-0.002*(exchange.fetch_free_balance()[symbol_2]))
                    print(f"sleeping for {str(stoptime)} secondes...\n")
                    time.sleep(stoptime)
                    stoptime+=300
                    price_list=[]
                    break  # Exit the loop after selling

            # Sleep for a while before the next check
            # time.sleep(10)

    # Example usage
    if __name__ == '__main__':
        trading_bot()
