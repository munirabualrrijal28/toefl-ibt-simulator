import random
from typing import List, Optional
from uuid import UUID, uuid4
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, col
from .database import engine, create_db_and_tables
from .models import TestSession, SectionState, QuestionItem, UserResponse, SubmitPayload, SessionStartResponse

app = FastAPI(title="2026 TOEFL iBT Simulator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

def get_session():
    with Session(engine) as session:
        yield session

@app.post("/session/start", response_model=SessionStartResponse)
def start_session(db: Session = Depends(get_session)):
    session = TestSession(id=uuid4())
    db.add(session)
    db.commit()
    db.refresh(session)
    
    reading_state = SectionState(
        session_id=session.id,
        section_name="Reading",
        stage="ROUTING"
    )
    db.add(reading_state)
    db.commit()
    return SessionStartResponse(id=session.id, created_at=session.created_at)

@app.get("/session/{session_id}/current-state", response_model=SectionState)
def get_current_state(session_id: UUID, db: Session = Depends(get_session)):
    state = db.exec(
        select(SectionState)
        .where(SectionState.session_id == session_id)
        .where(SectionState.is_done == False)
    ).first()
    
    if not state:
        sections_done = db.exec(
            select(SectionState.section_name)
            .where(SectionState.session_id == session_id)
            .where(SectionState.is_done == True)
        ).all()
        
        next_section_name = None
        if "Reading" not in sections_done: next_section_name = "Reading"
        elif "Listening" not in sections_done: next_section_name = "Listening"
        elif "Writing" not in sections_done: next_section_name = "Writing"
        elif "Speaking" not in sections_done: next_section_name = "Speaking"
        
        if next_section_name:
            new_state = SectionState(
                session_id=session_id,
                section_name=next_section_name,
                stage="ROUTING" if next_section_name in ["Reading", "Listening"] else "FIXED"
            )
            db.add(new_state)
            db.commit()
            db.refresh(new_state)
            return new_state
        else:
            raise HTTPException(status_code=404, detail="Test completed")
    
    return state

@app.get("/session/{session_id}/next-item", response_model=QuestionItem)
def get_next_item(session_id: UUID, db: Session = Depends(get_session)):
    current_state = get_current_state(session_id, db)
    
    # Get answered question IDs as strings for reliable comparison
    answered_rows = db.exec(
        select(UserResponse.question_id).where(UserResponse.session_id == session_id)
    ).all()
    answered_id_strings = [str(qid) for qid in answered_rows]
    
    pool = "ROUTING"
    if current_state.stage == "ADAPTIVE_A_STANDARD": pool = "STANDARD"
    elif current_state.stage == "ADAPTIVE_B_HARD": pool = "HARD"
    elif current_state.stage == "FIXED": pool = "FIXED"

    # Get ALL items in this section+pool
    all_pool_items = db.exec(
        select(QuestionItem)
        .where(QuestionItem.section == current_state.section_name)
        .where(QuestionItem.difficulty_pool == pool)
    ).all()
    
    # Filter out answered items using string comparison (reliable across DB backends)
    available_items = [item for item in all_pool_items if str(item.id) not in answered_id_strings]
    
    if not available_items:
        if current_state.stage == "ROUTING":
            calculate_routing(current_state, session_id, db)
            return get_next_item(session_id, db)
        else:
            current_state.is_done = True
            db.add(current_state)
            db.commit()
            return get_next_item(session_id, db)

    return random.choice(available_items)

def calculate_routing(state: SectionState, session_id: UUID, db: Session):
    responses = db.exec(
        select(UserResponse).where(UserResponse.session_id == session_id)
        .join(QuestionItem).where(QuestionItem.section == state.section_name)
        .where(QuestionItem.difficulty_pool == "ROUTING")
    ).all()
    
    if not responses:
        state.stage = "ADAPTIVE_A_STANDARD"
    else:
        correct_count = sum(1 for r in responses if r.is_correct)
        accuracy = correct_count / len(responses)
        state.stage = "ADAPTIVE_B_HARD" if accuracy >= 0.70 else "ADAPTIVE_A_STANDARD"
    
    db.add(state)
    db.commit()

@app.post("/session/{session_id}/submit-response")
def submit_response(session_id: UUID, payload: SubmitPayload, db: Session = Depends(get_session)):
    item = db.get(QuestionItem, payload.question_id)
    if not item:
        raise HTTPException(status_code=404, detail="Question not found")
        
    is_correct = False
    if item.correct_answer_key:
        is_correct = (payload.text_payload == item.correct_answer_key)
    else:
        is_correct = True
        
    response = UserResponse(
        session_id=session_id,
        question_id=payload.question_id,
        text_payload=payload.text_payload,
        audio_payload_path=payload.audio_path,
        is_correct=is_correct
    )
    db.add(response)
    db.commit()
    return {"status": "success", "is_correct": is_correct}

@app.get("/session/{session_id}/score")
def get_final_score(session_id: UUID, db: Session = Depends(get_session)):
    states = db.exec(select(SectionState).where(SectionState.session_id == session_id)).all()
    
    total_band = 0
    for state in states:
        if not state.band_score:
            if state.stage == "ADAPTIVE_B_HARD":
                state.band_score = round(random.uniform(4.0, 6.0) * 2) / 2
            else:
                state.band_score = round(random.uniform(1.0, 4.5) * 2) / 2
        total_band += state.band_score
        db.add(state)
    
    avg_score = total_band / max(len(states), 1)
    session = db.get(TestSession, session_id)
    if session:
        session.overall_score = round(avg_score * 2) / 2
        session.is_completed = True
        db.add(session)
        db.commit()
        
    return {
        "overall_score": session.overall_score if session else 0,
        "sections": [{"id": s.id, "section_name": s.section_name, "band_score": s.band_score, "stage": s.stage} for s in states]
    }
