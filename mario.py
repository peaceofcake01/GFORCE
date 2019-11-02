from cs50 import get_int

# Prompt user for number between 1 and 8
while True:
    n = get_int("Height: ")
    if n >= 1 and n <= 8:
        break

r = 1
d = 0
h = 0

# go through a loop and write out hashes and spaces
for r in range(n):
    print(" " * (n - r - 1), "#" * (r + 1))

