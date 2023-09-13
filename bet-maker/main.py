from fastapi import FastAPI


app = FastAPI(
    title="Bet-maker",
)


@app.get("/health")
async def check_health():
    return {
        "ok": True
    }
