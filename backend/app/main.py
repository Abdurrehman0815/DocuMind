from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import Base, engine
from app.config.settings import settings
from app.routes.router import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.on_event("startup")
def on_startup() -> None:
    import app.models.document  # noqa: F401
    import app.models.chunk  # noqa: F401
    from app.services.scheduler import start_scheduler

    Base.metadata.create_all(bind=engine)
    start_scheduler()


@app.get("/")
def root():
    return {"message": "AI Life Admin Agent backend running"}
