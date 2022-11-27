import os

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class SessionManager:

    test_db_path = '/tmp/sanic-express-test.db'
    docker_db_path = "/data/main.db"
    local_db_path = "data/main.db"
    connDict = {"main": f"sqlite:///{docker_db_path if os.environ.get('USER') == 'root' else local_db_path}",
                "test": f"sqlite:///{test_db_path}",
                }

    connDictAsync = {"main": f"sqlite+aiosqlite:///{docker_db_path if os.environ.get('USER') == 'root' else local_db_path}",
                     "test": f"sqlite+aiosqlite:///{test_db_path}",
                     "memory": "sqlite+aiosqlite://",
                     }

    def __init__(self):
        self.engines = {}
        self.sessionMakers = {}
        self.async_engines = {}
        self.async_sessions = {}

    def get_engine(self, env="main", echo=False):

        if env not in self.engines:
            connString = self.connDict[env]
            engine = create_engine(connString, echo=echo, pool_pre_ping=True)
            self.engines[env] = engine

        else:
            engine = self.engines[env]

        return engine

    def get_session(self, env="main", echo=False):

        if env not in self.sessionMakers:
            engine = self.get_engine(env, echo)
            Session = sessionmaker(engine)
            self.sessionMakers[env] = Session

        else:
            Session = self.sessionMakers[env]

        return Session()

    def get_async_engine(self, env="main", echo=False):

        if env not in self.async_engines:
            connString = self.connDictAsync[env]
            engine = create_async_engine(connString, echo=echo, pool_pre_ping=True)
            self.async_engines[env] = engine
        else:
            engine = self.async_engines[env]

        return engine

    def get_async_session(self, env="main", echo=False):

        if env not in self.async_sessions:
            engine = self.get_async_engine(env, echo)
            self.async_sessions[env] = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        return self.async_sessions[env]()

    def create_tables(self, env="main"):
        engine = self.get_engine(env)
        Base.metadata.create_all(engine)

    def delete_test_db(self):
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    async def async_create_tables(self, env="main"):
        engine = self.get_async_engine(env)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


session_manager = SessionManager()


def get_session(env="main", echo=False):
    return session_manager.get_session(env, echo=echo)


def get_async_session(env="main", echo=False):
    return session_manager.get_async_session(env, echo=echo)
