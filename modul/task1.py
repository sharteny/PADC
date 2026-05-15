#!/usr/bin/python3

import requests
from tabulate import tabulate
import time

URL = "https://api.coingecko.com/api/v3/coins/markets"

def get_crypto_data():
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1,
        "sparkline": False
    }

    res = requests.get(URL, params=params)
    return res.json()


def display_data(data):
    table = []

    for coin in data:
        table.append([
            coin["name"],
            coin["symbol"].upper(),
            f"${coin['current_price']:,}",
            f"${coin['market_cap']:,}",
            f"${coin['total_volume']:,}",
            f"{coin['price_change_percentage_24h']:.2f}%"
        ])

    headers = [
        "Name",
        "Symbol",
        "Price",
        "Market Cap",
        "Volume",
        "24h Change"
    ]

    print(tabulate(table, headers=headers, tablefmt="grid"))


def filter_data(data):
    print("\n=== FILTER OPTIONS ===")
    print("1. Search by name")
    print("2. Price > X")
    print("3. Market Cap > X")
    print("4. Volume > X")
    print("5. 24h Change > X")
    print("6. Show all")

    choice = input("Choose option: ")

    filtered = data

    if choice == "1":
        text = input("Enter name: ").lower()
        filtered = [
            coin for coin in data
            if text in coin["name"].lower()
        ]

    elif choice == "2":
        x = float(input("Price greater than: "))
        filtered = [
            coin for coin in data
            if coin["current_price"] > x
        ]

    elif choice == "3":
        x = float(input("Market Cap greater than: "))
        filtered = [
            coin for coin in data
            if coin["market_cap"] > x
        ]

    elif choice == "4":
        x = float(input("Volume greater than: "))
        filtered = [
            coin for coin in data
            if coin["total_volume"] > x
        ]

    elif choice == "5":
        x = float(input("24h Change greater than: "))
        filtered = [
            coin for coin in data
            if coin["price_change_percentage_24h"] > x
        ]

    return filtered


def main():
    while True:
        print("\nLoading cryptocurrency data...\n")

        data = get_crypto_data()

        filtered_data = filter_data(data)

        display_data(filtered_data)

        again = input("\nRefresh data? (y/n): ")

        if again.lower() != "y":
            print("Program ended.")
            break

        time.sleep(2)


if __name__ == "__main__":
    main()
