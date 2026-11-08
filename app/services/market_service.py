from app.clients.polymarket import fetch_active_markets, fetch_market_by_id


async def list_markets(active: bool | None = None):
    response_market = await fetch_active_markets()
    if active is None:
        return response_market
    another_list = []
    for active_market in response_market:
        if active_market["active"] == active:
            another_list.append(active_market)
    return another_list

async def get_market_by_id(market_id: str):
    response_market_id = await fetch_market_by_id(market_id)
    return response_market_id