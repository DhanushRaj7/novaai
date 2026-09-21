from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from app.api.processes import router as process_router
from app.api.initiatives import router as initiative_router
from app.api.initiative_links import router as initiative_link_router
from app.api.initiative_dependencies import router as initiative_dependency_router
from app.db.database import get_db
from app.api.enterprise_intelligence import router as enterprise_intelligence_router


app = FastAPI(title="NovaAI")


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(process_router)
app.include_router(initiative_router)
app.include_router(initiative_link_router)
app.include_router(initiative_dependency_router)
app.include_router(enterprise_intelligence_router)


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/health/db")
def database_health(
    db: Session = Depends(get_db),
):
    result = db.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar(),
    }