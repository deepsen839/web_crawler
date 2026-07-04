from typing import List, Dict

from app.services.serper import SerperClient
from app.schemas.competitor import Competitor

class CompetitorService:
    """
    Finds and validates competitors using:
    1. AI suggestions
    2. Serper search
    """

    def __init__(self):
        self.serper = SerperClient()

    async def get_competitors(
        self,
        company_name: str,
        industry: str,
        country: str,
        ai_competitors: List[str],
    ) -> List[Dict]:

        competitors = []

        seen = set()

        # -----------------------------
        # AI Suggested Competitors
        # -----------------------------
        for company in ai_competitors:

            company = company.strip()

            if not company:
                continue

            if company.lower() in seen:
                continue

            seen.add(company.lower())

            website = await self.serper.find_official_website(company)

            competitors.append(
                Competitor(
                    name=company,
                    website=website,
                    source="Serper",
                )
            )

        # -----------------------------
        # Serper Search
        # -----------------------------
        query = f"{industry} companies in {country}"

        result = await self.serper.search(query)

        organic = result.get("organic", [])

        for item in organic:

            title = item.get("title", "")

            link = item.get("link", "")

            if not title:
                continue

            company = title.split("|")[0].split("-")[0].strip()

            if company.lower() == company_name.lower():
                continue

            if company.lower() in seen:
                continue

            seen.add(company.lower())

            competitors.append(
                Competitor(
                    name=company,
                    website=website,
                    source="Serper",
                )
            )

        return competitors