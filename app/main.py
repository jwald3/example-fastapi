from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models            # retrieve all working model schemas
from .database import engine    # brings in connection to DB
from .routers import post, user, auth, vote
from .config import settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]             # should be as narrow as possible

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # sets what origin sites requests can be made from
    allow_credentials=True,
    allow_methods=['*'],    # restricts types of HTTP methods
    allow_headers=['*'],    # restricts headers
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello world"}
