from dataclasses import dataclass
from typing import List


@dataclass
class Product:
    name: str
    price: float
    stock: int
    category: str


class Inventory:
    def __init__(self) -> None:
        self.products: List[Product] = []

    def add(self, product: Product) -> None:
        # Add a product to inventory
        self.products.append(product)

    def remove(self, name: str) -> None:
        # Remove product by name
        self.products = [p for p in self.products if p.name != name]

    def search(self, keyword: str) -> List[Product]:
        # Search products by name
        return [p for p in self.products if keyword.lower() in p.name.lower()]

    def show_all(self) -> None:
        # Display all products
        for p in self.products:
            print(p)


if __name__ == "__main__":
    inv = Inventory()

    # Add products
    inv.add(Product("Laptop", 80000, 10, "Electronics"))
    inv.add(Product("Phone", 30000, 5, "Electronics"))
    inv.add(Product("Shirt", 1500, 20, "Clothing"))

    print("All Products:")
    inv.show_all()

    print("\nSearch 'lap':")
    print(inv.search("lap"))

    print("\nAfter deleting 'Phone':")
    inv.remove("Phone")
    inv.show_all()
