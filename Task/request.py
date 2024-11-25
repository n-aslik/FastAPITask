import httpx
import asyncio

async def send_request():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:8000/api/")
        response1 = await client.get("http://127.0.0.1:8000/endpoint")
        response2 = await client.get("http://127.0.0.1:8000/endpoint")
        print(response.json())
        print(response1.json())
        print(response2.json())

asyncio.run(send_request())