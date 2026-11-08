from httpx import AsyncClient


async def fetch_active_markets():
    async with AsyncClient() as client:
        response = await client.get(
            "https://gamma-api.polymarket.com/markets/keyset",
            params={"closed": False, "limit": 20},
        )
        response.raise_for_status()
        data = response.json()
        return data["markets"]

async def fetch_market_by_id(market_id: str):
    async with AsyncClient() as client:
        response = await client.get(
            f"https://gamma-api.polymarket.com/markets/{market_id}"
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()