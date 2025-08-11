# main.py
import asyncio
from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Text, ForeignKey, Boolean, JSON, DateTime, Integer

# ------------------------------------------------------------------
# 1.  DATABASE  (copied from your working file)
# ------------------------------------------------------------------
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
    name: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text)
    password: Mapped[str] = mapped_column(Text)
    profile_picture: Mapped[str] = mapped_column(Text)
    is_ai_user: Mapped[bool] = mapped_column(Boolean, default=False)
    persona_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ChatLogAI05(Base):
    __tablename__ = "ai05_chat_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("ai05_users.id"))
    message: Mapped[str] = mapped_column(Text)
    is_ai_response: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


# ------------------------------------------------------------------
# 2.  CREATE TABLES & DEFAULT USER
# ------------------------------------------------------------------
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All ai05 tables created successfully!")


async def ensure_default_user():
    async with async_session() as s:
        user = await s.get(UserAI05, 1)
        if user is None:
            s.add(
                UserAI05(
                    id=1,
                    name="System",
                    email="system@ai05.local",
                    password="",
                    profile_picture="",
                    persona_json={},
                )
            )
            await s.commit()


# ------------------------------------------------------------------
# 3.  AGENT IMPORTS
# ------------------------------------------------------------------
from myagents.atlasfx_agent import run_agent as run_atlasfx
from myagents.cryptonova_agent import run_agent as run_cryptonova
from myagents.janemacro_agent import run_agent as run_janemacro
from myagents.maxmentor_agent import run_agent as run_maxmentor
from myagents.quantedge_agent import run_agent as run_quantedge


# ------------------------------------------------------------------
# 4.  HELPER — SAVE TO DB
# ------------------------------------------------------------------
async def save_chat(message: str, user_id: int = 1):
    async with async_session() as session:
        log = ChatLogAI05(user_id=user_id, message=message, is_ai_response=True)
        session.add(log)
        await session.commit()


# ------------------------------------------------------------------
# 5.  MAIN FLOW
# ------------------------------------------------------------------
async def main():
    await create_tables()
    await ensure_default_user()

    agents_prompts = [
        ("AtlasFX", run_atlasfx, "What’s the FX summary for USD/JPY?"),
        ("CryptoNova", run_cryptonova, "What’s the latest crypto update?"),
        ("JaneMacro", run_janemacro, "Give me a macroeconomic update"),
        ("MaxMentor", run_maxmentor, "How should I start learning AI today?"),
        ("QuantEdge", run_quantedge, "Give me today's market update"),
    ]

    for name, runner, prompt in agents_prompts:
        print(f"🟦 Running {name} Agent...")
        result = await runner(prompt)
        print(f"Result from {name}:\n{result}\n")
        await save_chat(f"[{name}] {result}")


# ------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())