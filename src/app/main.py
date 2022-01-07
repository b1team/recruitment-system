from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from src.app.api.v1 import api as api_v1

app = FastAPI()

origins = [
   "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1.router, prefix="/api/v1")


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
