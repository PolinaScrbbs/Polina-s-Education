from fastapi import FastAPI

from .user.router import router as userRouter
from .auth.router import router as authRouter
from .group.router import router as groupRouter
from .practice.router import router as practiceRouter
from .module.router import router as moduleRouter
from .content.router import router as contentRouter
from .lesson.router import router as lessonRouter

app = FastAPI(
    title="Polina's Education",
    description="API for Conducting Practice",
    version="2.2.8",
)


app.include_router(authRouter, tags=["Auth"])
app.include_router(userRouter, tags=["User"])
app.include_router(groupRouter, tags=["Group"])
app.include_router(practiceRouter, tags=["Practice"])
app.include_router(moduleRouter, tags=["Module"])
app.include_router(lessonRouter, tags=["Lesson"])
app.include_router(contentRouter, tags=["Content"])
