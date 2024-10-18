from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite async engine
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)

# SessionLocal is an async session generator
SessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session
