import db.records

from db.base import get_async_session, get_session, session_manager


def create_tables(env="main"):
    session_manager.create_tables(env)


async def async_create_tables(env="memory"):
    await session_manager.async_create_tables(env)
