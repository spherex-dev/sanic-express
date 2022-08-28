import db.records

from .base import get_async_session, get_session, session_manager


def create_tables(env="main"):
    session_manager.create_tables(env)
