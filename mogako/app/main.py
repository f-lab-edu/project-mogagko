from dataclasses import asdict

import uvicorn

from fastapi import FastAPI

from mogako.app.api import api_router
from mogako.app.config import conf
from mogako.db.database import db


def create_app():
    c = conf()
    app = FastAPI()
    app.include_router(api_router)
    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
