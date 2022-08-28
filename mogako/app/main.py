from fastapi import FastAPI

from mogako.app.api import api_router
from mogako.db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router)
