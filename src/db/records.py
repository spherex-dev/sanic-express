###############################################################################
# Copyright (C) 2022, created on August 21, 2022
# Written by Justin Ho
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3 as published by
# the Free Software Foundation.
#
# This source code is distributed in the hope that it will be useful and
# without warranty or implied warranty of merchantability or fitness for a
# particular purpose.
###############################################################################

import datetime
import os

from sqlalchemy import (JSON, Column, DateTime, Index, Integer, String,
                        UniqueConstraint, insert, select, update, and_)
from sqlalchemy.exc import IntegrityError

from .base import Base


class Record(Base):
    """Simple class to store records"""
    __tablename__ = "record"

    id = Column(Integer, primary_key=True)
    path = Column(String)
    key = Column(String)
    data = Column(JSON)
    created = Column(DateTime, default=datetime.datetime.now)

    uc_path_key = UniqueConstraint(path, key)
    ix_created = Index("ix_created", created)

    @staticmethod
    def path_split(path):
        split = path.rsplit("/", 1)
        if len(split) == 1:
            split.insert(0, '')
        return split

    @classmethod
    def get_query(cls, path):
        path, key = cls.path_split(path)
        query = select(cls.data, cls.created).\
            filter(cls.path == path).\
            filter(cls.key == key)
        return query

    @classmethod
    def get_item(cls, session, path: str):
        record = session.execute(cls.get_query(path)).first()
        if record:
            data, created = record
            return {"data": data, "created": created}
        else:
            return None

    @classmethod
    async def async_get_item(cls, session, path: str):
        cursor = await session.execute(cls.get_query(path))
        record = cursor.first()
        if record:
            data, created = record
            return {"data": data, "created": created}
        else:
            return None

    @classmethod
    def put_query(cls, path, data):
        path, key = cls.path_split(path)
        query = insert(cls).values(
            path=path, key=key, data=data)
        return query

    @classmethod
    def update_query(cls, path, data):
        path, key = cls.path_split(path)
        query = update(cls).where(and_(cls.path == path, cls.key == key)).values(data=data)
        return query

    @classmethod
    def put_item(cls, session, path: str, data: dict):
        with session.begin():
            try:
                session.execute(cls.put_query(path, data))
                session.commit()
            except IntegrityError:
                session.execute(cls.update_query(path, data))
                session.commit()

    @classmethod
    async def async_put_item(cls, session, path: str, data: dict):
        async with session.begin():
            try:
                await session.execute(cls.put_query(path, data))
                await session.commit()
            except IntegrityError:
                await session.execute(cls.update_query(path, data))
                await session.commit()

    @classmethod
    def list_query(cls, path):
        return select(cls.key).\
            filter(cls.path == path)

    @classmethod
    def list_items(cls, session, path):
        return [os.path.join(path, key[0]) for key in session.execute(cls.list_query(path)).fetchall()]

    @classmethod
    async def async_list_items(cls, session, path):
        cursor = await session.execute(cls.list_query(path))
        return [os.path.join(path, key[0]) for key in cursor.fetchall()]

    @classmethod
    def delete_query(cls, path):
        path, key = cls.path_split(path)
        query = cls.__table__.delete().where(and_(cls.path == path, cls.key == key))
        return query

    @classmethod
    def delete_item(cls, session, path: str):
        with session.begin():
            session.execute(cls.delete_query(path))
            session.commit()

    @classmethod
    async def async_delete_item(cls, session, path: str):
        async with session.begin():
            await session.execute(cls.delete_query(path))
            await session.commit()
