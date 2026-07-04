import json
from typing import Dict, Any

import httpx

from app.config import settings


class OpenRouterClient:
    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "AI Company Research Assistant",
        }

    async def analyze_company(
        self,
        company_name: str,
        website: str,
        crawled_content: Dict[str, str],
        public_search: Dict[str, Any],
        model: str | None = None,
    ) -> Dict[str, Any]:

        selected_model = (
            model
            if model
            else settings.OPENROUTER_DEFAULT_MODEL
        )

        website_content = "\n\n".join(
            [
                f"PAGE: {url}\n{text[:1500]}"
                for url, text in crawled_content.items()
            ]
        )

        search_content = json.dumps(
            public_search,
            indent=2,
        )

        prompt = f"""
You are an expert business research analyst.

Analyze the following company.

Company Name:
{company_name}

Website:
{website}

Website Content:
{website_content}

Public Search Results:
{search_content}

Return ONLY valid JSON.

{{
    "company_summary":"",
    "phone_number":"",
    "address":"",
    "products_services":[],
    "pain_points":[],
    "industry":"",
    "country":"",
    "competitor_suggestions":[]
}}

Rules

- Return JSON only.
- No markdown.
- No explanation.
- Missing values should be "".
"""

        payload = {
            "model": selected_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": 0.2,
        }

        async with httpx.AsyncClient(
            timeout=120,
        ) as client:

            import asyncio

            for attempt in range(3):

                response = await client.post(
                    self.BASE_URL,
                    headers=self.headers,
                    json=payload,
                )

                if response.status_code == 429:

                    retry = int(
                        response.headers.get(
                            "Retry-After",
                            "5",
                        )
                    )

                    print(f"Rate limited. Retrying in {retry} seconds...")

                    await asyncio.sleep(retry)

                    continue

                break

        # response.raise_for_status()
        if response.status_code != 200:
            print(response.status_code)
            print(response.text)
            raise Exception(response.text)

        result = response.json()

        content = (
            result["choices"][0]["message"]["content"]
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:
            return json.loads(content)

        except Exception:

            return {
                "company_summary": content,
                "phone_number": "",
                "address": "",
                "products_services": [],
                "pain_points": [],
                "industry": "",
                "country": "",
                "competitor_suggestions": [],
            }