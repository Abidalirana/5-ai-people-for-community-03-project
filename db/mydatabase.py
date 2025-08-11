# db.py  (keep only what we actually use)
from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Text, ForeignKey, Boolean, JSON, DateTime, Integer

DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/ai05"
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass


class UserAI05(Base):
    __tablename__ = "ai05_users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text, default="System")
    email: Mapped[str] = mapped_column(Text, default="system@ai05.local")
    password: Mapped[str] = mapped_column(Text, default="")
    profile_picture: Mapped[str] = mapped_column(Text, default="")
    is_ai_user: Mapped[bool] = mapped_column(Boolean, default=False)
    persona_json: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ChatLogAI05(Base):
    __tablename__ = "ai05_chat_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("ai05_users.id"))
    message: Mapped[str] = mapped_column(Text)
    is_ai_response: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All ai05 tables created successfully!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(create_tables())