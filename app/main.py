from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth import router as auth_router
from app.admin import router as admin_router

app = FastAPI(title="Backend Auth JSON")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tu peux restreindre ici en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"message": "Serveur backend prêt 🚀"}
