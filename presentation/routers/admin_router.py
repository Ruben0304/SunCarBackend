from fastapi import APIRouter

router = APIRouter()

@router.get("/admin")
async def say_hello():
    return {"message": f"Hello"}
