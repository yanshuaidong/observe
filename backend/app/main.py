from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.strategies import router as strategies_router
from .settings import get_settings


app = FastAPI(title="observe-backend")

s = get_settings()
cors_origins = s.cors_allow_origins if s.cors_allow_origins != ["*"] else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"ok": True}


app.include_router(strategies_router)

