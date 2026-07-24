
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import complaints


Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Complaint Management System")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(complaints.router)


@app.get("/")
def health():
    return {"status": "ok", "service": "complaint-management"}
