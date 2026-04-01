from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()


@app.get("/external-products")
async def get_products():
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get("https://fakestoreapi.com/products")

            if res.status_code != 200:
                raise HTTPException(
                    status_code=res.status_code,
                    detail="External API failed"
                )

            return res.json()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
