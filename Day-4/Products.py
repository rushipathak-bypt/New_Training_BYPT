from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    stock: int
    category: str

    def apply_discount(self, percent: float) -> None:
        """Apply discount if valid"""
        if 0 <= percent <= 100:
            self.price *= 1 - percent / 100
        else:
            raise ValueError("Discount must be between 0 and 100")

    def is_available(self) -> bool:
        """Check if product is in stock"""
        return self.stock > 0

    @property
    def formatted_price(self) -> str:
        """Return price in ₹ format"""
        return f"{self.price}Rs"

    def __str__(self) -> str:
        return f"{self.name} ({self.category}) - {self.formatted_price}"


class DigitalProduct(Product):
    def __init__(self, name: str, price: float, category: str):
        super().__init__(name, price, stock=0, category=category)

    def is_available(self) -> bool:
        """Digital products are always available"""
        return True


if __name__ == "__main__":
    # Physical product
    p1 = Product("Laptop", 80000, 10, "Electronics")
    print(p1)

    p1.apply_discount(10)
    print("After discount:", p1.formatted_price)
    print("Available:", p1.is_available())

    print()

    # Digital product
    d1 = DigitalProduct("Ebook", 500, "Education")
    print(d1)
    print("Available:", d1.is_available())
