"""Cha-ching."""

amount = int(input("Enter a sum: "))
coins = 0
available_coins = [1, 5, 10, 20, 50]

for i in available_coins[::-1]:
    if amount >= i:
        coins_count = amount // i
        coins += coins_count
        amount = amount % (coins_count * i)

print(f"Amount of coins needed: {coins}")
