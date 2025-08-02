from typing import AsyncGenerator
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Text, DateTime, ARRAY, Boolean, JSON, ForeignKey

# -------------------------
# DATABASE CONFIGURATION
# -------------------------
DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/ai05"
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# -------------------------
# BASE CLASS
# -------------------------
class Base(DeclarativeBase):
    pass

# -------------------------
# TABLE DEFINITIONS
# -------------------------

# 1. Users Table
class UserAI05(Base):
    __tablename__ = "ai05_users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text)
    password: Mapped[str] = mapped_column(Text)
    profile_picture: Mapped[str] = mapped_column(Text)
    is_ai_user: Mapped[bool] = mapped_column(Boolean, default=False)
    persona_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

# 2. AI Personas Table
class AIPersonaAI05(Base):
    __tablename__ = "ai05_ai_personas"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    bio: Mapped[str] = mapped_column(Text)
    tone: Mapped[str] = mapped_column(Text)
    specialty: Mapped[str] = mapped_column(Text)
    profile_picture: Mapped[str] = mapped_column(Text)
    prompt_template: Mapped[str] = mapped_column(Text)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

# 3. Posts Table
class PostAI05(Base):
    __tablename__ = "ai05_posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("ai05_users.id"))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

# 4. Comments Table
class CommentAI05(Base):
    __tablename__ = "ai05_comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("ai05_posts.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("ai05_users.id"))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

# 5. Chat Logs Table
class ChatLogAI05(Base):
    __tablename__ = "ai05_chat_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("ai05_users.id"))
    message: Mapped[str] = mapped_column(Text)
    is_ai_response: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

# 6. Feedback Table
class FeedbackAI05(Base):
    __tablename__ = "ai05_feedback"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("ai05_users.id"))
    feedback: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

# 7. Scheduled Jobs Table
class ScheduledJobAI05(Base):
    __tablename__ = "ai05_scheduled_jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    job_type: Mapped[str] = mapped_column(Text)
    scheduled_for: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(Text)

# -------------------------
# CREATE TABLES FUNCTION
# -------------------------
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All ai05 tables created successfully!")

# Optional: for testing directly
if __name__ == "__main__":
    import asyncio
    asyncio.run(create_tables())
