import requests

symbol = input("Enter stock symbol: ")

url = f"http://127.0.0.1:8000/price/{symbol}"

response = requests.get(url)

print("\n========= STOCK DATA AGENT =========")
print(response.json())
print("====================================")