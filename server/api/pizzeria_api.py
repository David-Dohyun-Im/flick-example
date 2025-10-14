import httpx


async def get_pizzerias(topping: str):
    """피자 가게 API 호출"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.example.com/pizzerias?topping={topping}"
        )
        response.raise_for_status()
        return response.json()

