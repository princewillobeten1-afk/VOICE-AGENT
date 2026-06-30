from __future__ import annotations

import asyncio
import httpx

BASE_URL = "http://127.0.0.1:8000/v1"


async def main() -> None:
    async with httpx.AsyncClient(timeout=20) as client:
        health = await client.get("http://127.0.0.1:8000/health")
        print("health", health.status_code, health.json())

        payload = {
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "password": "correct-horse-battery-staple",
            "organization_name": "Acme Co",
        }
        signup = await client.post(f"{BASE_URL}/auth/signup", json=payload)
        print("signup", signup.status_code)
        print(signup.text)

        signin = await client.post(f"{BASE_URL}/auth/signin", json={"email": payload["email"], "password": payload["password"]})
        print("signin", signin.status_code)
        print(signin.text)


if __name__ == "__main__":
    asyncio.run(main())