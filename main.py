

#********************************************************************************************************************************
#********************************************************************************************************************************
#********************************************************************************************************************************
#********************************************************************************************************************************
#********************************************************************************************************************************
#This code snippet is part of a method that processes a market feed response for a trading bot
# ********************************************************************************************************************************


import json
import os
from dhanhq import dhanhq, marketfeed
import time
from datetime import datetime
import stock_info_lookup as stock_info

class GridTradingBot:
    def __init__(self, client_id, access_token, symbol, quantity, top_price, bottom_price, grid_size, max_grid_levels, target_points=None):
        self.dhan = dhanhq(client_id, access_token)
        self.client_id = client_id
        self.access_token = access_token
        self.symbol = symbol
        self.quantity = quantity
        self.top_price = top_price
        self.bottom_price = bottom_price
        self.grid_size = grid_size
        self.max_grid_levels = max_grid_levels
        self.target_points = target_points
        self.grid_levels = self.create_grid_levels()
        self.placed_orders = {}  # Changed to dictionary
        self.current_price = None
        self.strategy_name = "Reliance Strategy"
        self.state_file = f"{self.strategy_name.replace(' ', '_')}_state.json"
        self.load_state()
        self.setup_market_feed()

    def create_grid_levels(self):
        grid_levels = []
        current_price = self.top_price
        while current_price >= self.bottom_price and len(grid_levels) < self.max_grid_levels:
            grid_levels.append(current_price)
            current_price -= self.grid_size
        return grid_levels

    def place_order(self, grid_level, transaction_type):
        self.dhan.place_order(
            security_id=self.symbol,
            exchange_segment=self.dhan.NSE,
            transaction_type=transaction_type,
            quantity=self.quantity,
            order_type=self.dhan.MARKET,
            product_type=self.dhan.MTF,
            price=0
        )
        print(f"Placing {transaction_type} order for {self.quantity} units of {self.symbol} at grid level {grid_level}")
        self.placed_orders[grid_level] = transaction_type  # Update dictionary
        self.save_state()

    def monitor_price_and_trade(self):
        start_time = datetime.strptime("09:16:00", "%H:%M:%S").time()
        end_time = datetime.strptime("15:30:00", "%H:%M:%S").time()

        while True:
            current_time = datetime.now().time()
            if start_time <= current_time <= end_time:
                try:
                    self.get_current_price()
                    if self.current_price is not None:
                        print(f"Current LTP of {self.symbol}: Rs {self.current_price}")
                        for grid_level in self.grid_levels:
                            if self.current_price <= grid_level and self.placed_orders.get(grid_level) != self.dhan.BUY:
                                self.place_order(grid_level, self.dhan.BUY)
                                print(f"Share purchased at grid level {grid_level}")
                            elif self.current_price >= grid_level + self.grid_size and self.placed_orders.get(grid_level) == self.dhan.BUY:
                                # Only sell if the current price is not above the top price
                                if self.current_price <= self.top_price:
                                    self.place_order(grid_level + self.grid_size, self.dhan.SELL)
                                    del self.placed_orders[grid_level]  # Remove from dictionary
                                    print(f"Share sold at grid level {grid_level + self.grid_size}")
                                else:
                                    print(f"Holding position as current price {self.current_price} is above top price {self.top_price}")
                except Exception as e:
                    print(f"Error getting current price: {e}")
                    self.reconnect_market_feed()  # Reconnect
            else:
                print("Outside trading hours. Waiting...")
            time.sleep(1)

    def save_state(self):
        state = {
            "placed_orders": self.placed_orders,
            "grid_levels": self.grid_levels,
            "current_price": self.current_price
        }
        with open(self.state_file, 'w') as f:
            json.dump(state, f)
        print(f"State saved to {self.state_file}")

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                state = json.load(f)
                self.placed_orders = state["placed_orders"]
                self.grid_levels = state["grid_levels"]
                self.current_price = state["current_price"]
            print(f"State loaded from {self.state_file}")
        else:
            print(f"No previous state found for {self.strategy_name}")

    def setup_market_feed(self):
        instruments = [(marketfeed.NSE, self.symbol, marketfeed.Ticker)]
        version = "v2"

        try:
            self.data = marketfeed.DhanFeed(self.client_id, self.access_token, instruments, version)
            print("Market feed setup complete.")
            self.data.run_forever()
        except Exception as e:
            print(f"Error setting up market feed: {e}")
            self.reconnect_market_feed()

    def reconnect_market_feed(self):
        print("Reconnecting market feed...")
        time.sleep(1)  # Wait for 5 seconds before reconnecting
        self.setup_market_feed()

    def get_current_price(self):
        try:
            response = self.data.get_data()
            if response:
                print(f"Market feed response: {response}")
                if isinstance(response, dict) and response.get('security_id') == int(self.symbol):
                    ltp = response.get('LTP')
                    if ltp:
                        self.current_price = float(ltp)
                        print(f"Updated current price of {self.symbol} to Rs {self.current_price}")
                        return self.current_price
                    else:
                        print("LTP not found in response")
                else:
                    print(f"Security ID {response.get('security_id')} does not match {self.symbol}")
            else:
                print("No response received")
        except Exception as e:
            print(f"Error getting current price: {e}")
            self.reconnect_market_feed()

# # Example usage
# if __name__ == "__main__":
#     bot = GridTradingBot(
#         client_id="your_client_id",
#         access_token="your_access_token",
#         symbol="HDFC",
#         quantity=10,
#         top_price=1290,
#         bottom_price=1200,
#         grid_size=10,
#         max_grid_levels=10
#     )
#     bot.monitor_price_and_trade()
# 
