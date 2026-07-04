from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.research import router as research_router

app = FastAPI(
    title="AI Company Research Assistant",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(research_router)


@app.get("/")
async def root():
    return {
        "message": "AI Company Research Assistant API",
        "status": "running",
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}