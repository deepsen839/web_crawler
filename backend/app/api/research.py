from tempfile import NamedTemporaryFile

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.schemas.company import CompanyResearchRequest
from app.services.research_service import ResearchService

router = APIRouter(
    prefix="/research",
    tags=["Research"],
)

service = ResearchService()


@router.post("")
async def research_company(
    request: CompanyResearchRequest,
):
    try:

        result = await service.research(
            company_input=request.company,
            applicant_name=request.applicant_name,
            applicant_email=request.applicant_email,
            discord_bot_token=request.discord_bot_token,
            discord_channel_id=request.discord_channel_id,
            model=request.model,
        )

        pdf = result.pop("pdf")

        with NamedTemporaryFile(
            delete=False,
            suffix=".pdf",
        ) as temp:

            temp.write(pdf.getvalue())

            pdf_path = temp.name

        result["download_url"] = (
            f"/research/pdf?path={pdf_path}"
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.get("/pdf")
async def download_pdf(path: str):

    return FileResponse(
        path=path,
        media_type="application/pdf",
        filename="company_report.pdf",
    )