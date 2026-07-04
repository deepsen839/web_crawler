from typing import List

from pydantic import BaseModel, Field


class CompanyResearchRequest(BaseModel):
    company: str = Field(
        ...,
        description="Company name or official website URL",
        examples=["Microsoft", "https://stripe.com"],
    )

    applicant_name: str = Field(
        default="",
        description="Applicant name",
    )

    applicant_email: str = Field(
        default="",
        description="Applicant email",
    )

    discord_bot_token: str = Field(
        default="",
        description="Discord Bot Token",
    )

    discord_channel_id: str = Field(
        default="",
        description="Discord Channel ID",
    )

    model: str | None = Field(
        default=None,
        description="OpenRouter model selected by the user",
    )


class CompanyInfo(BaseModel):
    company_name: str
    website: str

    phone_number: str = ""
    address: str = ""

    industry: str = ""
    country: str = ""

    company_summary: str = ""

    products_services: List[str] = []

    pain_points: List[str] = []


class ResearchResponse(BaseModel):
    company: CompanyInfo

    competitors: list

    crawled_pages: int

    download_url: str