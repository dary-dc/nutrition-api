from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def home():
    return {"message": "Welcome to the Nutrition API"}

@router.get("/health", tags=["monitoring"])
def health():
    return {"status": "ok"}
