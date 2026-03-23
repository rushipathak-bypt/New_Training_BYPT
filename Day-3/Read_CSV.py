import csv

products = []

with open("E:\\Python Trainee\\New Training\\Day-3\\products.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        row["price"] = int(row["price"])
        row["stock"] = int(row["stock"])
        products.append(row)

print(products)
print()

# Check Stocks
in_stock = [p for p in products if p["stock"] > 0]

print("In Stock items: ", in_stock)
print()

# Filter via Categories
categories = set(p["category"] for p in products)

grouped = {cat: [p for p in products if p["category"] == cat] for cat in categories}

print(grouped)
print()

# Sorting Products
sorted_products = sorted(products, key=lambda x: x["price"], reverse=True)

print(sorted_products)

# Discount Prices


def discount(*prices):
    return [p * 0.9 for p in prices]


# print(discount(100, 200, 300))

prices = [p["price"] for p in products]

discounted = discount(10, *prices)

print(discounted)

# Filter products of Electronics and Sale where sale condition which I have taken is stock < 10

electronics = {p["name"] for p in products if p["category"] == "Electronics"}

sale = {p["name"] for p in products if p["stock"] < 10}

common = electronics & sale

print("Electronics:", electronics)
print("Sale:", sale)
print("Common:", common)
