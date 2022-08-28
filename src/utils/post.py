from sanic.request import Request


def get_post_data(request: Request):
    if request.headers['content-type'].startswith("multipart/form-data"):
        return {k: v[0] for k, v in request.form.items()}
    elif request.headers['content-type'] == "application/json":
        return request.json
