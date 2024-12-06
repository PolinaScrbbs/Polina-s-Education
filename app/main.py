from quart import Quart
from .routers import index_router, auth_router, practice_router

app = Quart(__name__, static_folder="static", template_folder="templates")

app.register_blueprint(index_router)
app.register_blueprint(auth_router)
app.register_blueprint(practice_router)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
