from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models import Trace, LLMEvent
from app.schemas import TraceResponse

router = APIRouter()

@router.get("/", response_model=List[TraceResponse])
def list_traces(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Trace).order_by(Trace.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/{trace_id}")
def get_trace(trace_id: str, db: Session = Depends(get_db)):
    trace = db.query(Trace).filter(Trace.trace_id == trace_id).first()
    if not trace:
        raise HTTPException(status_code=404, detail="Trace not found")
    events = db.query(LLMEvent).filter(LLMEvent.trace_id == trace_id).all()
    return {"trace": trace, "events": events}