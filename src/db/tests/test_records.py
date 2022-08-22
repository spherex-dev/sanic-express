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

import unittest
from db.records import Record
from db.base import session_manager, get_session


class Test(unittest.TestCase):

    def setUp(self) -> None:
        session_manager.create_tables("test")

    def test_record(self):

        path = "test/path"
        path2 = "test/path2"
        data = {"a": 1, "b": 2}
        with get_session("test") as session:
            Record.put_item(session, path, data)

        with get_session("test") as session:
            record = Record.get_item(session, path)

        self.assertEqual(data, record["data"])

        data = {"a": 2, "b": 3}
        with get_session("test") as session:
            Record.put_item(session, path, data)
            Record.put_item(session, path2, data)
            record = Record.get_item(session, path)
            records = Record.list_items(session, "test")

        self.assertEqual(data, record["data"])
        self.assertEqual(records, ['test/path', 'test/path2'])

        with get_session("test") as session:
            Record.delete_item(session, path2)
            records = Record.list_items(session, "test")

        self.assertEqual(records, ['test/path'])


if __name__ == "__main__":
    session_manager.delete_test_db()
    unittest.main()
    session_manager.delete_test_db()
