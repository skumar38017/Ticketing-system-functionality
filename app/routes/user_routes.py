#  app/routes/user_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.schemas import UserCreate, UserResponse
from app.curd_operation.user_curd import create_user, get_user_by_uuid, update_user, delete_user

router = APIRouter()

# Route to create a new user
@router.post("/register", response_model=UserResponse)
async def create_user_route(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db=db, user=user)

# Route to get a user by UUID
@router.get("/user/{uuid}", response_model=UserResponse)
async def get_user_route(uuid: str, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_uuid(db=db, uuid=uuid)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Route to update a user by UUID
@router.put("/user/{uuid}", response_model=UserResponse)
async def update_user_route(uuid: str, user: UserCreate, db: AsyncSession = Depends(get_db)):
    updated_user = await update_user(db=db, uuid=uuid, user=user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# Route to delete a user by UUID
@router.delete("/user/{uuid}", response_model=dict)
async def delete_user_route(uuid: str, db: AsyncSession = Depends(get_db)):
    success = await delete_user(db=db, uuid=uuid)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
