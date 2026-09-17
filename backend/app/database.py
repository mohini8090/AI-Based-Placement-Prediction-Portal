"""
MongoDB connection via Motor (the async driver FastAPI pairs well with).
No ORM/migrations — collections are created implicitly on first insert.
"""
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

client = AsyncIOMotorClient(settings.mongo_uri)
db = client[settings.mongo_db_name]

users_collection = db["users"]
resumes_collection = db["resumes"]
predictions_collection = db["predictions"]
career_recommendations_collection = db["career_recommendations"]


async def init_indexes():
    """Creates the indexes each module relies on. Safe to call every
    startup — Mongo no-ops if an equivalent index already exists."""
    await users_collection.create_index("email", unique=True)
    await resumes_collection.create_index("user_id")
    await predictions_collection.create_index("user_id")
    await predictions_collection.create_index("created_at")
    await career_recommendations_collection.create_index("user_id")


def get_database():
    """FastAPI dependency for routers that want the raw database handle."""
    return db
