#  app/curd_operation/user_curd.py

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.database.models import User
from app.schemas.schema import UserCreate, UserResponse

# Create a new user
async def create_user(db: AsyncSession, user: UserCreate) -> UserResponse:
    try:
        db_user = User(
            name=user.name,
            email=user.email,
            phone_no=user.phone_no,
            is_active=user.is_active
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return UserResponse.from_orm(db_user)
    except SQLAlchemyError as e:
        await db.rollback()
        raise e

# Get user by UUID
async def get_user_by_uuid(db: AsyncSession, uuid: str) -> UserResponse:
    try:
        query = select(User).filter(User.uuid == uuid)
        result = await db.execute(query)
        user = result.scalars().first()
        if user:
            return UserResponse.from_orm(user)
        return None
    except SQLAlchemyError as e:
        raise e

# Update user information
async def update_user(db: AsyncSession, uuid: str, user: UserCreate) -> UserResponse:
    try:
        query = select(User).filter(User.uuid == uuid)
        result = await db.execute(query)
        db_user = result.scalars().first()
        if db_user:
            db_user.name = user.name
            db_user.email = user.email
            db_user.phone_no = user.phone_no
            db_user.is_active = user.is_active
            await db.commit()
            await db.refresh(db_user)
            return UserResponse.from_orm(db_user)
        return None
    except SQLAlchemyError as e:
        await db.rollback()
        raise e

# Delete a user by UUID
async def delete_user(db: AsyncSession, uuid: str) -> bool:
    try:
        query = select(User).filter(User.uuid == uuid)
        result = await db.execute(query)
        db_user = result.scalars().first()
        if db_user:
            await db.delete(db_user)
            await db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
