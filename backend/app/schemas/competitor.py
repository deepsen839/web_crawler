from pydantic import BaseModel, HttpUrl


class Competitor(BaseModel):
    """
    Represents a competitor company.
    """

    name: str

    website: str = ""

    source: str = "AI"


class CompetitorResponse(BaseModel):
    competitors: list[Competitor]