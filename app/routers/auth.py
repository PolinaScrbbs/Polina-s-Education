from quart import Blueprint, render_template, request, redirect, url_for
from .. import responses as response


auth_router = Blueprint("auth", __name__)


@auth_router.route("/registration", methods=["GET", "POST"])
async def registration():
    if request.method == "POST":
        # Ожидаем завершения получения данных формы
        form = await request.form

        # Теперь можно извлечь данные из form
        username = form["username"]
        password = form["password"]
        confirm_password = form["confirm_password"]
        fullname = form["fullname"]

        # Логика обработки данных, например, проверка пароля
        if password != confirm_password:
            return "Passwords do not match", 400

        # Логика для создания пользователя (например, в базе данных)
        status = await response.registraion(
            username, password, confirm_password, fullname
        )

        if status == 201:
            # Редирект на страницу входа после успешной регистрации
            return redirect(url_for("auth.login"))
        else:
            return await render_template(
                "registrations.html",
                username=username,
                fullname=fullname,
                error_message="Registration failed",
            )

    return await render_template("registrations.html")


@auth_router.route("/login")
async def login():
    return await render_template("login.html")
