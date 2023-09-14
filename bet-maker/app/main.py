from fastapi import FastAPI

from .routes import router

app = FastAPI(
    title="Bet-maker",
)


@app.get("/health")
async def check_health():
    return {"ok": True}


app.include_router(router)
