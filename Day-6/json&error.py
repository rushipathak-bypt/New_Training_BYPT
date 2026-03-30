import requests
import json
import logging
import csv


#  Setup logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    # format="%(asctime)s - %(levelname)s - %(message)s"
)


#  Custom Exception
class ProductAPIError(Exception):
    pass


#  Step 1: Call API
def fetch_products(url: str) -> list:
    try:
        logging.info("Calling API...")
        response = requests.get(url)

        if response.status_code != 200:
            raise ProductAPIError(f"API failed with status {response.status_code}")

        return response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        raise ProductAPIError("Failed to fetch products")


#  Step 2: Save JSON
def save_to_json(data: list, filename: str) -> None:
    with open(filename, "w") as f:
        json.dump(data, f)
    logging.info("Saved data to JSON")


#  Step 3: Read + Filter
def filter_products(filename: str) -> list:
    with open(filename, "r") as f:
        products = json.load(f)

    # FakeStore API price is in USD → assume ₹ conversion (~80)
    return [p for p in products if p["price"] * 80 < 1000]


#  Step 4: Print Names
def print_product_names(products: list) -> None:
    print("\nProducts under ₹1000:")
    for p in products:
        print(p["title"])


#  Step 5: CSV Read & Write
def csv_filter(input_file: str, output_file: str) -> None:
    filtered = []

    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if float(row["price"]) < 1000:
                filtered.append(row)

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=filtered[0].keys())
        writer.writeheader()
        writer.writerows(filtered)

    logging.info("Filtered CSV written")


#  MAIN EXECUTION
if __name__ == "__main__":
    URL = "https://fakestoreapi.com/products"

    try:
        data = fetch_products(URL)
        save_to_json(data, "products.json")

        filtered_products = filter_products("products.json")
        print_product_names(filtered_products)

    except ProductAPIError as e:
        print("Error:", e)
        logging.error(str(e))

    # CSV part (optional test)
    csv_filter("input.csv", "output.csv")
