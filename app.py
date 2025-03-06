import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from module import (
    dentalstall_module
)
from db.database import JSONDatabase

app = FastAPI(title="Atlys Scraper")
db = JSONDatabase()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# routing swagger api documentation to default path
@app.get("/")
def index():
    return RedirectResponse(url="/docs")

# Attaching a dentalstall scaper router file for layered architecture, Example - can accomodate multiple router for diff scrapers
app.include_router(dentalstall_module.router, prefix="/dentalstall", tags=["Dentalstall Data"])

# health check for the application database, can also do it for in-memory redis db
@app.get("/health")
def health_check():
    db_status = db.health_check()
    return db_status

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port="8000")
