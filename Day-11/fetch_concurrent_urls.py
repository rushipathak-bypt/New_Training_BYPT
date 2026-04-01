import asyncio
import httpx

urls = [
    "https://fakestoreapi.com/products/1",
    "https://fakestoreapi.com/products/2",
    "https://fakestoreapi.com/products/3",
    "https://fakestoreapi.com/products/4",
    "https://fakestoreapi.com/products/5",
]


async def fetch(url):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            print("URL:", url)
            print("Status:", response.status_code)

            if response.status_code != 200:
                print(f"Failed: {url}")
                return None

            return response.json()

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


async def main():
    tasks = [fetch(url) for url in urls]
    results = await asyncio.gather(*tasks)

    for r in results:
        print(r["title"])


asyncio.run(main())
