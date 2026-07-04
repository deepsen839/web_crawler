from io import BytesIO
from typing import List, Dict

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from app.schemas.competitor import Competitor
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PDFGenerator:

    def __init__(self):

        styles = getSampleStyleSheet()

        self.title_style = styles["Heading1"]
        self.title_style.alignment = TA_CENTER

        self.heading_style = styles["Heading2"]

        self.normal_style = styles["BodyText"]

        logger.info("PDF Generator initialized.")

    def _section(self, story, title: str):

        story.append(
            Paragraph(
                title,
                self.heading_style,
            )
        )

        story.append(
            Spacer(1, 0.15 * inch)
        )

    def _field(
        self,
        story,
        key: str,
        value: str,
    ):

        story.append(
            Paragraph(
                f"<b>{key}</b><br/>{value or 'N/A'}",
                self.normal_style,
            )
        )

        story.append(
            Spacer(1, 0.12 * inch)
        )

    def generate(
        self,
        company: Dict,
        competitors: List[Competitor],
    ) -> BytesIO:

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)

        story = []

        # -------------------------------------------------
        # Title
        # -------------------------------------------------

        story.append(
            Paragraph(
                "AI Company Research Report",
                self.title_style,
            )
        )

        story.append(
            Spacer(1, 0.30 * inch)
        )

        # -------------------------------------------------
        # Company Information
        # -------------------------------------------------

        self._section(
            story,
            "Company Information",
        )

        self._field(
            story,
            "Company Name",
            company.get("company_name", ""),
        )

        self._field(
            story,
            "Website",
            company.get("website", ""),
        )

        self._field(
            story,
            "Phone Number",
            company.get("phone_number", ""),
        )

        self._field(
            story,
            "Address",
            company.get("address", ""),
        )

        self._field(
            story,
            "Industry",
            company.get("industry", ""),
        )

        self._field(
            story,
            "Country",
            company.get("country", ""),
        )

        # -------------------------------------------------
        # Summary
        # -------------------------------------------------

        self._section(
            story,
            "Company Summary",
        )

        story.append(
            Paragraph(
                company.get(
                    "company_summary",
                    "",
                ),
                self.normal_style,
            )
        )

        story.append(
            Spacer(1, 0.25 * inch)
        )

        # -------------------------------------------------
        # Products & Services
        # -------------------------------------------------

        self._section(
            story,
            "Products & Services",
        )

        for item in company.get(
            "products_services",
            [],
        ):

            story.append(
                Paragraph(
                    f"• {item}",
                    self.normal_style,
                )
            )

        story.append(
            Spacer(1, 0.25 * inch)
        )

        # -------------------------------------------------
        # Pain Points
        # -------------------------------------------------

        self._section(
            story,
            "AI Generated Pain Points",
        )

        for item in company.get(
            "pain_points",
            [],
        ):

            story.append(
                Paragraph(
                    f"• {item}",
                    self.normal_style,
                )
            )

        story.append(
            Spacer(1, 0.25 * inch)
        )

        # -------------------------------------------------
        # Competitors
        # -------------------------------------------------

        self._section(
            story,
            "Competitors",
        )

        data = [
            [
                "Company",
                "Website",
                "Source",
            ]
        ]

        for competitor in competitors:

            data.append(
                [
                    competitor.name,
                    competitor.website,
                    competitor.source,
                ]
            )

        table = Table(
            data,
            colWidths=[
                2.0 * inch,
                3.5 * inch,
                1.3 * inch,
            ],
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#2563EB"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        1,
                        colors.black,
                    ),
                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, -1),
                        colors.whitesmoke,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, 0),
                        10,
                    ),
                ]
            )
        )

        story.append(table)

        doc.build(story)

        buffer.seek(0)

        logger.info("PDF generated successfully.")

        return buffer