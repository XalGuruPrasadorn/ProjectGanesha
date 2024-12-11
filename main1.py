
import subprocess
import json
from main import GridTradingBot
import stock_info_lookup as stock_info  # Assuming this module fetches security ID by name

def get_user_input(prompt, cast_type=str):
    while True:
        try:
            return cast_type(input(prompt))
        except ValueError:
            print(f"Invalid input. Please enter a valid {cast_type.__name__} value.")

def main():
    client_id = "1105337404"
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM1NDgzODIyLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNTMzNzQwNCJ9.A6eMs0kbqrE12-bLFZCnlBEV4iSRKB3H1_T61RNpsXl-OzAGRoG1G-XTRCLgKa2hz8ehZVGYaFNAIb3nrDtWWg"
    stock_name = input("Enter the stock name (e.g., 'HDFCBANK'): ")
    symbol = stock_info.fetch_security_id_by_name(stock_name, 'EQUITY')[1][0]
    quantity = get_user_input("Enter quantity: ", int)
    top_price = get_user_input("Enter the top price: ", float)
    bottom_price = get_user_input("Enter the bottom price: ", float)
    grid_size = get_user_input("Enter the grid size: ", float)
    max_grid_levels = get_user_input("Enter the maximum number of grid levels: ", int)
    target_points = get_user_input("Enter the target points (or press Enter for None): ", float) if input("Do you have target points? (y/n): ").lower() == 'y' else None

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
    main()


