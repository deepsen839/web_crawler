import httpx

from app.config import settings
from app.utils.logger import get_logger
from app.utils.cache import cached
logger = get_logger(__name__)

class SerperClient:
    BASE_URL = "https://google.serper.dev"

    def __init__(self):
        self.headers = {
            "X-API-KEY": settings.SERPER_API_KEY,
            "Content-Type": "application/json",
        }
        # logger.info(f"Searching Serper for {query}")

    @cached
    async def search(self, query: str) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{self.BASE_URL}/search",
                headers=self.headers,
                json={"q": query},
            )

            response.raise_for_status()
            return response.json()

    async def find_official_website(self, company_name: str) -> str | None:
        result = await self.search(f"{company_name} official website")

        organic = result.get("organic", [])

        if not organic:
            return None

        return organic[0].get("link")

    async def search_company(self, company: str) -> dict:
        return await self.search(company)

    async def search_competitors(self, company: str) -> dict:
        return await self.search(f"{company} competitors")