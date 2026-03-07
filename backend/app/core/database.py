from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# PostgreSQL
engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# MongoDB
mongo_client = AsyncIOMotorClient(settings.MONGO_URL)
mongo_db = mongo_client["prodtool"]
raw_messages_collection = mongo_db["raw_messages"]

def get_mongo_db():
    return mongo_db
