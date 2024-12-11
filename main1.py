import os
from dotenv import load_dotenv
import json
from main import GridTradingBot
import stock_info_lookup as stock_info  # Assuming this module fetches security ID by name
from keep_alive import keep_alive  # Import keep_alive function

# Load environment variables from .env file
# load_dotenv()

def get_user_input(prompt, cast_type=str):
    while True:
        try:
            return cast_type(input(prompt))
        except ValueError:
            print(f"Invalid input. Please enter a valid {cast_type.__name__} value.")

def main():
    client_id = os.getenv("DHAN_CLIENT_ID")
    access_token = os.getenv("DHAN_ACCESS_TOKEN")
    
    if not client_id or not access_token:
        print("Error: DHAN_CLIENT_ID and DHAN_ACCESS_TOKEN environment variables are required.")
        return

    # stock_name = input("Enter the stock name (e.g., 'HDFCBANK'): ")
    # symbol = stock_info.fetch_security_id_by_name(stock_name, 'EQUITY')[1][0]
    # quantity = get_user_input("Enter quantity: ", int)
    # top_price = get_user_input("Enter the top price: ", float)
    # bottom_price = get_user_input("Enter the bottom price: ", float)
    # grid_size = get_user_input("Enter the grid size: ", float)
    # max_grid_levels = get_user_input("Enter the maximum number of grid levels: ", int)
    # target_points = get_user_input("Enter the target points (or press Enter for None): ", float) if input("Do you have target points? (y/n): ").lower() == 'y' else None

    stock_name = "RELIANCE"
    symbol = stock_info.fetch_security_id_by_name(stock_name, 'EQUITY')[1][0]
    quantity = 1
    top_price = 1900.0
    bottom_price = 1800.0
    grid_size = 10.0
    max_grid_levels = 100
    target_points = None
    
    # Store the inputs in a dictionary
    config = {
        "client_id": client_id,
        "access_token": access_token,
        "stock_name": stock_name,
        "symbol": symbol,
        "quantity": quantity,
        "top_price": top_price,
        "bottom_price": bottom_price,
        "grid_size": grid_size,
        "max_grid_levels": max_grid_levels,
        "target_points": target_points,
    }

    # Create the bot instance
    bot = GridTradingBot(
        client_id=config['client_id'],
        access_token=config['access_token'],
        symbol=config['symbol'],
        quantity=config['quantity'],
        top_price=config['top_price'],
        bottom_price=config['bottom_price'],
        grid_size=config['grid_size'],
        max_grid_levels=config['max_grid_levels'],
        target_points=config.get('target_points'),
    )

    # Start monitoring and trading
    print("Starting the Grid Trading Bot...")
    bot.monitor_price_and_trade()

if __name__ == "__main__":
    keep_alive()  # Start the keep-alive server
    main()
