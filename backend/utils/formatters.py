# backend/utils/formatters.py

def format_price(price):
    return f"${price:,.2f}"

def format_stock(stock):
    return f"{stock} unidades"

def format_datetime(dt):
    return dt.strftime("%d/%m/%Y %H:%M")
