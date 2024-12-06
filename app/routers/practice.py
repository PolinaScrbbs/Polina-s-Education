from typing import Optional
from quart import Blueprint, render_template, redirect, url_for

practice_router = Blueprint("practice", __name__)


@practice_router.route("/practices")
async def practices(token: Optional[str] = None):
    if not token:
        return redirect(url_for("auth.registration"))
    return await render_template("practice.html")
