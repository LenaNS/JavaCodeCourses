import asyncio
import json
from typing import Tuple

from aiohttp import ClientSession


async def fetch_url(
    session: ClientSession, url: str, semaphore: int
) -> Tuple[str, int]:
    try:
        async with semaphore:
            async with session.get(url, timeout=5 * 60) as response:
                return url, response.status
    except Exception:
        return url, 0


async def fetch_urls(urls_file_path: str, file_path: str) -> None:
    semaphore = asyncio.Semaphore(5)
    with open(urls_file_path, "r") as urls_file:
        for url in urls_file:
            async with ClientSession() as session:
                task = await fetch_url(session, url, semaphore)
                with open(file_path, "a") as file:
                    json.dump({"url": task[0], "status_code": task[1]}, file)
                    file.write("\n")


asyncio.run(fetch_urls("urls.txt", "results.json"))
