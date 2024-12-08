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

    if current_user["group_id"] is None:
        return redirect(url_for("group.group_application_submission", token=token))

    status, group = await response.get_group_practice(token)

    context = {"current_user": current_user, "group": group}

    return await render_template("practice.html", **context)
