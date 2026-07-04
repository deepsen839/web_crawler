import httpx


class DiscordService:
    BASE_URL = "https://discord.com/api/v10"

    def __init__(
        self,
        bot_token: str,
        channel_id: str,
    ):
        self.bot_token = bot_token
        self.channel_id = channel_id

    @property
    def enabled(self) -> bool:
        return bool(self.bot_token and self.channel_id)

    async def send_report(
        self,
        applicant_name: str,
        applicant_email: str,
        company_name: str,
        company_website: str,
        pdf_bytes: bytes,
    ) -> bool:

        if not self.enabled:
            return False

        url = f"{self.BASE_URL}/channels/{self.channel_id}/messages"

        headers = {
            "Authorization": f"Bot {self.bot_token}",
        }

        content = f"""
**Company Research Report**

**Applicant Name:** {applicant_name}
**Applicant Email:** {applicant_email}

**Company:** {company_name}
**Website:** {company_website}
"""

        files = {
            "files[0]": (
                "company_report.pdf",
                pdf_bytes,
                "application/pdf",
            )
        }

        data = {
            "content": content,
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                url,
                headers=headers,
                data=data,
                files=files,
            )

        response.raise_for_status()

        return True