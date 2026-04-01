def price_generator(prices):
    for p in prices:
        yield p


prices = [50, 100, 75, 425, 500, 200, 350, 250, 300]

gen = price_generator(prices)

print(next(gen))
print(next(gen))
