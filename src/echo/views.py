from sanic.blueprints import Blueprint
from sanic.request import Request
from sanic.response import json
from utils.post import get_post_data


bp = Blueprint("echo", url_prefix="api/echo/")


@bp.route("echo", methods=["POST"])
async def echo(request: Request):
    if request.method == "POST":
        return json(get_post_data(request))
    return json({"fail": True})
