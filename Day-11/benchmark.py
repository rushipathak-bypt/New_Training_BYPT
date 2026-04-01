import asyncio
import httpx
import time
import requests

urls = [
    "https://fakestoreapi.com/products/1",
    "https://fakestoreapi.com/products/2",
    "https://fakestoreapi.com/products/3",
    "https://fakestoreapi.com/products/4",
    "https://fakestoreapi.com/products/5",
]


# Sync Version
def fetch_sync():
    start = time.time()
    for url in urls:
        requests.get(url)
    print("Sync time: ", time.time() - start)


# Async version
async def fetch_async():
    start = time.time()

    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        await asyncio.gather(*tasks)

    print("Async time: ", time.time() - start)


fetch_sync()
asyncio.run(fetch_async())
