from quart import Blueprint, render_template, request, redirect, url_for
from .. import responses as response


auth_router = Blueprint("auth", __name__)


@auth_router.route("/registration", methods=["GET", "POST"])
async def registration():
    if request.method == "POST":
        form = await request.form

        username = form["username"]
        password = form["password"]
        confirm_password = form["confirm_password"]
        fullname = form["fullname"]

        if password != confirm_password:
            return "Passwords do not match", 400

        status = await response.registraion(
            username, password, confirm_password, fullname
        )

        if status == 201:
            return redirect(url_for("auth.login"))
        else:
            return await render_template(
                "registrations.html",
                username=username,
                fullname=fullname,
                error_message="Registration failed",
            )

    return await render_template("registrations.html")


@auth_router.route("/login", methods=["GET", "POST"])
async def login():
    if request.method == "POST":
        form = await request.form

        username = form["username"]
        password = form["password"]

        status, token = await response.login(username, password)

        if status in [200, 201]:
            return redirect(url_for("practice.practices", token=token["access_token"]))
        else:
            return await render_template("login.html", username=username)
    return await render_template("login.html")
