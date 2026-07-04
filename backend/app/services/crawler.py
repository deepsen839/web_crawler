from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
import httpx

from app.utils.logger import get_logger
from app.utils.cache import cached

logger = get_logger(__name__)


class WebsiteCrawler:
    IMPORTANT_KEYWORDS = [
        "about",
        "company",
        "product",
        "products",
        "service",
        "services",
        "solution",
        "solutions",
        "contact",
        "pricing",
    ]

    IGNORE_KEYWORDS = [
        "login",
        "signin",
        "signup",
        "register",
        "privacy",
        "terms",
        "cookie",
        "cart",
        "checkout",
        "account",
    ]

    def __init__(self):
        self.visited = set()
    @cached
    async def crawl(self, website: str) -> dict:
        """
        Crawl the company website and return
        structured content.
        """

        pages = await self.discover_pages(website)

        content = {}
        logger.info(f"Crawling {website}")

        for page in pages:
            text = await self.extract_text(page)

            if text:
                content[page] = text

        return content

    async def discover_pages(self, website: str) -> list[str]:
        """
        Discover important internal pages.
        """

        discovered = []

        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            response = await client.get(website)

        soup = BeautifulSoup(response.text, "lxml")

        domain = urlparse(website).netloc

        discovered.append(website)

        for link in soup.find_all("a", href=True):

            href = link["href"]

            url = urljoin(website, href)

            parsed = urlparse(url)

            if parsed.netloc != domain:
                continue

            if any(word in url.lower() for word in self.IGNORE_KEYWORDS):
                continue

            if any(word in url.lower() for word in self.IMPORTANT_KEYWORDS):

                if url not in discovered:
                    discovered.append(url)

        return discovered

    async def extract_text(self, url: str) -> str:

        if url in self.visited:
            return ""

        self.visited.add(url)

        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            response = await client.get(url)

        soup = BeautifulSoup(response.text, "lxml")

        for tag in soup(
            [
                "script",
                "style",
                "noscript",
                "svg",
                "header",
                "footer",
                "nav",
                "form",
            ]
        ):
            tag.decompose()

        text = soup.get_text(separator="\n")

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        return "\n".join(lines)