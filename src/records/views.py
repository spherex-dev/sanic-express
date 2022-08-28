from db.base import get_async_session
from db.records import Record
from sanic.blueprints import Blueprint
from sanic.request import Request
from sanic.response import json

bp = Blueprint("record", url_prefix="api/record/")


@bp.route("put_item", methods=["POST"])
async def put_item(request: Request):
    if request.method == "POST":
        env = request.app.config.get("DB_ENV")
        async with get_async_session(env) as session:
            await Record.async_put_item(session,
                                        request.json["path"],
                                        request.json["data"])
            return json({"status": "success"})
    else:
        return json({"error": "invalid request"})


@bp.route("delete_item", methods=["POST"])
async def delete_item(request):
    if request.method == "POST":
        env = request.app.config.get("DB_ENV")
        async with get_async_session(env) as session:
            await Record.async_delete_item(session,
                                           request.json["path"])
            return json({"status": "success"})
    else:
        return json({"error": "invalid request"})


@bp.route("get_item", methods=["POST"])
async def get_item(request):
    if request.method == "POST":
        env = request.app.config.get("DB_ENV")
        async with get_async_session(env) as session:
            record = await Record.async_get_item(session,
                                                 request.json["path"])
            if record:
                record["created"] = record["created"].timestamp()
            return json(record)
    else:
        return json({"error": "invalid request"})


@bp.route("list_items", methods=["POST"])
async def list_items(request):
    if request.method == "POST":
        env = request.app.config.get("DB_ENV")
        async with get_async_session(env) as session:
            records = await Record.async_list_items(session,
                                                    request.json["path"])
            print("records", records)
            return json(records)
    else:
        return json({"error": "invalid request"})
