from quart import Blueprint, render_template, redirect, url_for, request
from .. import responses as response

practice_router = Blueprint("practice", __name__)


@practice_router.route("/practices")
async def practices():
    token = request.args.get("token")

    if not token:
        return redirect(url_for("auth.registration"))
    
    status, current_user = await response.get_current_user(token)

    if status != 200:
        return redirect(url_for("auth.login"))
    
    context = {
        "current_user": current_user
    }

    return await render_template("practice.html", **context)
