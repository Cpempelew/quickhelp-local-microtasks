from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.routers import admin, ai, auth, categories, notifications, reviews, tasks, users
from app.services.seed_service import seed_database

app = FastAPI(title="QuickHelp API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    seed_database()


@app.get("/")
def root():
    return FileResponse("index.html")


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(reviews.router)
app.include_router(categories.router)
app.include_router(ai.router)
app.include_router(notifications.router)
app.include_router(admin.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
