from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.process import Process
from app.schemas.process import ProcessCreate, ProcessResponse

from app.services.process_analyzer import analyze_process
from app.services.analysis_persistence import persist_analysis


router = APIRouter(
    prefix="/processes",
    tags=["Processes"],
)


@router.post(
    "",
    response_model=ProcessResponse,
)
def create_process(
    process_data: ProcessCreate,
    db: Session = Depends(get_db),
):
    process = Process(
        value_chain_stage_id=process_data.value_chain_stage_id,
        name=process_data.name,
        description=process_data.description,
        business_purpose=process_data.business_purpose,
        current_challenges=process_data.current_challenges,
    )

    db.add(process)
    db.commit()
    db.refresh(process)

    return process


@router.get(
    "",
    response_model=list[ProcessResponse],
)
def get_processes(
    db: Session = Depends(get_db),
):
    result = db.execute(
        select(Process).order_by(Process.id)
    )

    return result.scalars().all()


@router.get(
    "/{process_id}",
    response_model=ProcessResponse,
)
def get_process(
    process_id: int,
    db: Session = Depends(get_db),
):
    process = db.get(Process, process_id)

    if process is None:
        raise HTTPException(
            status_code=404,
            detail="Process not found",
        )

    return process


@router.post("/{process_id}/analyze")
def analyze_process_endpoint(
    process_id: int,
    db: Session = Depends(get_db),
):
    process = db.get(Process, process_id)

    if process is None:
        raise HTTPException(
            status_code=404,
            detail="Process not found",
        )

    analysis = analyze_process(process)

    process = persist_analysis(
        db=db,
        process=process,
        analysis=analysis,
    )

    return {
        "process_id": process.id,
        "process_name": process.name,
        "priority_score": process.priority_score,
        "summary": analysis.summary,
        "activities_created": len(analysis.activities),
        "ai_opportunities_created": len(
            analysis.ai_opportunities
        ),
    }