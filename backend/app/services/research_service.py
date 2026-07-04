from urllib.parse import urlparse

from app.services.serper import SerperClient
from app.services.crawler import WebsiteCrawler
from app.services.openrouter import OpenRouterClient
from app.services.competitors import CompetitorService
from app.services.pdf_generator import PDFGenerator
from app.services.discord_service import DiscordService

from app.utils.logger import get_logger

logger = get_logger(__name__)


class ResearchService:

    def __init__(self):
        self.serper = SerperClient()
        self.crawler = WebsiteCrawler()
        self.ai = OpenRouterClient()
        self.competitor_service = CompetitorService()
        self.pdf_generator = PDFGenerator()

    def _is_url(self, value: str) -> bool:
        parsed = urlparse(value)
        return bool(parsed.scheme and parsed.netloc)

    async def research(
        self,
        company_input: str,
        applicant_name: str,
        applicant_email: str,
        discord_bot_token: str,
        discord_channel_id: str,
        model: str | None = None,
    ):

        try:

            logger.info(f"Starting research for {company_input}")

            # ----------------------------------------
            # Step 1
            # ----------------------------------------

            if self._is_url(company_input):

                website = company_input.rstrip("/")

                domain = urlparse(website).netloc

                company_name = (
                    domain.replace("www.", "")
                    .split(".")[0]
                    .capitalize()
                )

            else:

                company_name = company_input.strip()

                website = await self.serper.find_official_website(
                    company_name
                )

                if website is None:
                    raise Exception(
                        "Official website not found."
                    )

            logger.info(f"Website: {website}")

            # ----------------------------------------
            # Step 2
            # ----------------------------------------

            public_info = await self.serper.search_company(
                company_name
            )

            logger.info("Public search completed.")

            # ----------------------------------------
            # Step 3
            # ----------------------------------------

            crawled_content = await self.crawler.crawl(
                website
            )

            logger.info(
                f"Crawled {len(crawled_content)} pages."
            )

            # ----------------------------------------
            # Step 4
            # ----------------------------------------

            ai_result = await self.ai.analyze_company(
                company_name=company_name,
                website=website,
                crawled_content=crawled_content,
                public_search=public_info,
                model=model,
            )

            logger.info("AI analysis completed.")

            # ----------------------------------------
            # Step 5
            # ----------------------------------------

            competitors = (
                await self.competitor_service.get_competitors(
                    company_name=company_name,
                    industry=ai_result.get(
                        "industry",
                        "",
                    ),
                    country=ai_result.get(
                        "country",
                        "",
                    ),
                    ai_competitors=ai_result.get(
                        "competitor_suggestions",
                        [],
                    ),
                )
            )

            logger.info(
                f"Found {len(competitors)} competitors."
            )

            # ----------------------------------------
            # Step 6
            # ----------------------------------------

            company = {
                "company_name": company_name,
                "website": website,
                "phone_number": ai_result.get(
                    "phone_number",
                    "",
                ),
                "address": ai_result.get(
                    "address",
                    "",
                ),
                "industry": ai_result.get(
                    "industry",
                    "",
                ),
                "country": ai_result.get(
                    "country",
                    "",
                ),
                "company_summary": ai_result.get(
                    "company_summary",
                    "",
                ),
                "products_services": ai_result.get(
                    "products_services",
                    [],
                ),
                "pain_points": ai_result.get(
                    "pain_points",
                    [],
                ),
            }

            # ----------------------------------------
            # Step 7
            # ----------------------------------------

            pdf = self.pdf_generator.generate(
                company=company,
                competitors=competitors,
            )

            logger.info("PDF generated.")

            # ----------------------------------------
            # Step 8
            # Discord
            # ----------------------------------------

            if (
                discord_bot_token
                and discord_channel_id
            ):

                discord = DiscordService(
                    bot_token=discord_bot_token,
                    channel_id=discord_channel_id,
                )

                await discord.send_report(
                    applicant_name=applicant_name,
                    applicant_email=applicant_email,
                    company_name=company_name,
                    company_website=website,
                    pdf_bytes=pdf.getvalue(),
                )

                logger.info(
                    "Discord notification sent."
                )

            logger.info(
                "Research completed successfully."
            )

            return {
                "company": company,
                "competitors": competitors,
                "crawled_pages": len(crawled_content),
                "pdf": pdf,
            }

        except Exception:

            logger.exception("Research failed.")

            raise