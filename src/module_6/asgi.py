import httpx
import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()

API_URL = "https://api.exchangerate-api.com/v4/latest/"


@app.get("/{currency}")
async def get_exchange_rate(currency: str):
    url = f"{API_URL}{currency.upper()}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=404, detail="Валюта не найдена")
        except httpx.RequestError:
            raise HTTPException(
                status_code=500, detail="Ошибка при получении данных из API"
            )
    return response.json()


if __name__ == "__main__":
    uvicorn.run(app="src.module_6.asgi:app")
