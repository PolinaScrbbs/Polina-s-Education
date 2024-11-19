from fastapi import FastAPI

from .auth.router import router as authRouter

app = FastAPI(
    title="Deyana Sinema",
    description="The API of a Small Cinema for Kittens",
    version="2.2.8",
)

app.include_router(authRouter, tags=["Auth"])
