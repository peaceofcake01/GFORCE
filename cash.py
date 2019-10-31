from cs50 import get_float

# obtain float for change
while True:
    n = get_float("Change Owed?\n")
    if n > 0:
        break

# get float in integer form
penny = 100 * n

newPenny0 = round(penny)

newPenny = int(newPenny0)

# use floor division and then add up all types of coins
quarter = newPenny // 25
remainquarter = newPenny % 25

dime = remainquarter // 10
remaindime = remainquarter % 10

nickel = remaindime // 5
remainnickel = remaindime % 5

penny = remainnickel // 1

totalCoins = quarter + dime + nickel + penny

print(f"The total number of coins is {totalCoins}")
