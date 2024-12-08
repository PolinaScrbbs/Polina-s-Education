from quart import Blueprint, render_template, redirect, url_for, request
from .. import responses as response

group_router = Blueprint("group", __name__)


@group_router.route("/group/application/submission")
async def group_application_submission():
    token = request.args.get("token")

    if not token:
        return redirect(url_for("auth.registration"))
    
    status, current_user = await response.get_current_user(token)

    if status != 200:
        return redirect(url_for("auth.login"))
    
    status, specializations = await response.get_specializations_for_applications(token)
    
    context = {
        "current_user": current_user,
        "specializations": specializations
    }

    return await render_template("group_application_submission.html", **context)