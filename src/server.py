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

import logging
import os
from importlib import import_module

from sanic import Sanic

logger = logging.getLogger(__name__)


class Server:

    def __init__(self, name, env="main"):
        self.name = name
        self.env = env
        self.settings = {"host": "0.0.0.0", "port": 5005}
        self.app = Sanic(name=name)
        self.app.config["DB_ENV"] = env

        self.blueprints = ["records", "echo"]

        self.log_format = "%(asctime)s [%(levelname)s]: %(message)s"
        self.log_path = "sanic.log"
        self.log_level = "INFO"

    def setup_logs(self):
        level = getattr(logging, self.log_level)
        logging.basicConfig(filename=self.log_path, format=self.log_format, level=level)

    def setup_blueprints(self):
        for bp in self.blueprints:
            try:
                module = import_module(f"{bp}.views")
                self.app.blueprint(module.bp)
            except ModuleNotFoundError:
                print("failed to load blueprint %s" % bp)
                logger.warning("failed to load blueprint %s", bp)
                pass

    def setup_cors(self):
        from cors.headers import add_cors_headers
        from cors.options import setup_options

        # setup cors to some domain name or "*" for any
        if not os.environ.get("CORS"):
            return
        self.app.register_listener(setup_options, "before_server_start")
        self.app.register_middleware(add_cors_headers, "response")

    def setup(self):
        self.setup_logs()
        self.setup_blueprints()
        self.setup_cors()

    def run(self, auto_reload=True):

        self.setup()
        self.app.run(auto_reload=auto_reload, **self.settings)

    def test_app(self) -> Sanic:
        self.setup_blueprints()
        self.app.config["DB_ENV"] = "test"
        return self.app


if __name__ == "__main__":
    from db import create_tables
    create_tables()
    os.environ["CORS"] = "http://localhost"
    server = Server("sanic")
    server.run(auto_reload=True)
