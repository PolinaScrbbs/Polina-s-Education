from typing import Optional
from quart import Blueprint, redirect, render_template, url_for

index_router = Blueprint("index", __name__)


@index_router.route("/")
async def index(token: Optional[str] = None):
    if token:
        return redirect(url_for("practice.practices"))
    return await render_template("index.html")
