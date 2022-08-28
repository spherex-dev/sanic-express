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

import os
import unittest
from functools import cached_property

from db.base import session_manager
from db.records import Record
from server import Server


class Test(unittest.TestCase):

    def setUp(self) -> None:
        os.environ['CORS'] = '*'
        self.server = Server("test", env="test")

    @cached_property
    def app(self):
        return self.server.test_app()

    def post(self, *args, server_kwargs={"motd": False}, **kwargs):
        return self.app.test_client.post(*args, server_kwargs=server_kwargs, **kwargs)

    def get(self, *args, server_kwargs={"motd": False}, **kwargs):
        return self.app.test_client.get(*args, server_kwargs=server_kwargs, **kwargs)

    def test_record(self):
        data = {"name": "bob", "age": 23}
        _, response = self.post("/api/record/put_item", json={"path": "user/bob", "data": data})
        _, response = self.post("/api/record/get_item", json={"path": "user/bob"})
        self.assertEqual(response.json["data"], data)
        _, response = self.post("/api/record/list_items", json={"path": "user"})
        self.assertEqual(response.json, ['user/bob'])
        _, response = self.post("/api/record/delete_item", json={"path": "user/bob"})
        _, response = self.post("/api/record/list_items", json={"path": "user"})
        self.assertEqual(response.json, [])


if __name__ == "__main__":
    session_manager.delete_test_db()
    session_manager.create_tables("test")

    # table is not created without some dummy record
    with session_manager.get_session("test") as session:
        Record.put_item(session, "test/test", {"test": "test"})
        Record.delete_item(session, "test/test")
    unittest.main()
