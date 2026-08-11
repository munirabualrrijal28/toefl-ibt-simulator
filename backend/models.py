from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship, JSON

class TestSession(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    overall_score: Optional[float] = Field(default=None)
    is_completed: bool = Field(default=False)

    sections: List["SectionState"] = Relationship(back_populates="session")
    responses: List["UserResponse"] = Relationship(back_populates="session")

class SectionState(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: UUID = Field(foreign_key="testsession.id")
    section_name: str  # Reading, Listening, Speaking, Writing
    stage: str = Field(default="ROUTING")  # ROUTING, ADAPTIVE_A_STANDARD, ADAPTIVE_B_HARD, FIXED
    raw_score: float = Field(default=0.0)
    band_score: Optional[float] = Field(default=None)
    is_done: bool = Field(default=False)

    session: TestSession = Relationship(back_populates="sections")

class QuestionItem(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    section: str
    task_type: str  # COMPLETE_WORDS, BUILD_SENTENCE, LISTEN_REPEAT, WRITE_EMAIL, etc.
    difficulty_pool: str  # ROUTING, STANDARD, HARD
    content_meta: Dict[str, Any] = Field(default_factory=dict, sa_type=JSON)
    correct_answer_key: Optional[str] = None


class UserResponse(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    session_id: UUID = Field(foreign_key="testsession.id")
    question_id: UUID = Field(foreign_key="questionitem.id")
    text_payload: Optional[str] = None
    audio_payload_path: Optional[str] = None
    is_correct: Optional[bool] = None

    session: TestSession = Relationship(back_populates="responses")

class SubmitPayload(SQLModel):
    question_id: UUID
    text_payload: Optional[str] = None
    audio_path: Optional[str] = None

class SessionStartResponse(SQLModel):
    id: UUID
    created_at: datetime
