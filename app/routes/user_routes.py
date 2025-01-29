# app/routes/user_routes.py

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.schemas import UserCreate, UserResponse, UserBase  # These should now be available
from app.curd_operation.user_curd import create_user, get_user_by_uuid, update_user, delete_user
from pydantic import EmailStr
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse
from app.config import config
import logging
from app.utils.redis_data_storage import store_data_in_redis

router = APIRouter()

# Set up logging
logger = logging.getLogger("uvicorn.error")

# Route to create a new user
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
    description="Create a new user for the ticketing system and store user information in the database",
)
async def create_user_route(
    name: str = Form(..., description="Name of the user `admin`"),
    email: EmailStr = Form(..., description="Valid email address of the user `admin@admin.com`"),
    phone_no: str = Form(..., description="Phone number of the user `91 99999 99999` or `+91-99999 99999`"),
    is_active: bool = Form(True, description="User status, active or not"),
    db: AsyncSession = Depends(get_db),
) -> JSONResponse:
    """
    Handle user registration via a form in the browser.
    """
    try:
        # Create a Pydantic UserCreate model
        user_data = UserCreate(
            name=name,
            email=email,
            phone_no=phone_no,
            is_active=is_active,  # Default value is set here
        )
        
        # Temporarily store the data in Redis for 5 minutes
        redis_key = f"user_data_{phone_no}"  # Using phone number as the key
        store_data_in_redis(redis_key, user_data.model_dump(), expiration=config.expiration_time)  

        # # Call the CRUD function to create a user in the database
        # user = await create_user(db=db, user=user_data)
        # Log the event
        logger.info(f"User data temporarily stored in Redis for phone number: {phone_no}")

        # Respond back with success message
        return JSONResponse(content={"message": "User data stored temporarily in Redis."})
    
    # except SQLAlchemyError as e:
    #     logger.error(f"SQLAlchemyError: {str(e)}")
    #     raise HTTPException(status_code=500, detail="An error occurred while creating the user.")
    # except Exception as e:
    #     logger.error(f"Exception: {str(e)}")
    #     raise HTTPException(status_code=500, detail="An unexpected error occurred.")
    
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
    
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