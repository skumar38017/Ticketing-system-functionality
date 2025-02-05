# app/routes/user_routes.py

from fastapi import APIRouter, Depends, HTTPException, Form, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from starlette.responses import JSONResponse
import logging
import os

from app.database.database import get_db
from app.schemas import UserCreate, UserResponse
from app.config import config
from app.utils.redis_data_storage import RedisDataStorage
from app.curd_operation.user_curd import UserCRUD
from app.services.otp_service import OTPService
from app.utils.generate_otp import generate_otp
from app.workers.celery_app import trigger_task_and_get_id

class UserRoutes:
    def __init__(self):
        self.router = APIRouter()
        self.otp_service = OTPService()
        self.user_crud = UserCRUD()
        self.redis_data_storage = RedisDataStorage()
        self.logger = logging.getLogger("uvicorn.error")
        self._setup_routes()

    def _setup_routes(self):
        """
        Registers all routes in the APIRouter.
        """
        self.router.post(
            "/register",
            response_model=UserResponse,
            status_code=201,
            description="Create a new user for the ticketing system and store user information in the database",
        )(self.create_user_route)

        self.router.get(
            "/user/{uuid}",
            response_model=UserResponse,
            description="Retrieve a user by UUID"
        )(self.get_user_route)

        self.router.put(
            "/user/{uuid}",
            response_model=UserResponse,
            description="Update a user by UUID"
        )(self.update_user_route)

        self.router.delete(
            "/user/{uuid}",
            response_model=dict,
            description="Delete a user by UUID"
        )(self.delete_user_route)

    async def create_user_route(
        self,
        request: Request,
        name: str = Form(..., description="Name of the user `admin`"),
        email: EmailStr = Form(..., description="Valid email address of the user `admin@admin.com`"),
        phone_no: str = Form(..., description="Phone number of the user `91 99999 99999` or `+91-99999 99999` or `99999999999`"),
        db: AsyncSession = Depends(get_db),
    ) -> JSONResponse:
        """
        Handle user registration via a form in the browser.
        """
        try:
            # Step 1: Prepare user data
            user_data = {"name": name, "email": email, "phone_no": phone_no}
    
            # Step 2: Generate OTP
            otp = generate_otp()
    
            # Step 3: Manage session
            session = getattr(request.state, "session", None)
            if session is None or "session_id" not in session:
                session_id = os.urandom(24).hex()
                request.state.session = {"session_id": session_id}
            else:
                session_id = session["session_id"]
    
            # Step 4: Generate Redis key
            redis_key = RedisDataStorage.generate_redis_key(name=name, email=email, phone_no=phone_no)
    
            # Step 5: Store data in Redis
            redis_data = {
                "name": name,
                "email": email,
                "phone_no": phone_no,
                "otp": otp,
            }
            RedisDataStorage.store_data_in_redis(
                redis_key,
                redis_data,
                session_id=session_id,
                expiration=config.expiration_time,
            )
    
            # Step 6: Trigger OTP task asynchronously
            task_id = await self.otp_service.send_otp(phone_no=phone_no, name=name, otp=otp)
            self.logger.info(f"OTP generated for {phone_no}, task_id: {task_id}")
    
            # Step 7: Respond with task information
            return JSONResponse(
                content={
                    "message": "OTP sent and user data stored temporarily in Redis.",
                    "redis_key": redis_key,
                    "task_id": task_id,
                },
                headers={"Set-Cookie": f"session_id={session_id}; HttpOnly"},
            )
    
        except Exception as e:
            self.logger.error(f"Error during user registration: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")
            
    async def get_user_route(self, uuid: str, db: AsyncSession = Depends(get_db)) -> UserResponse:
        """
        Retrieve a user by UUID.
        """
        try:
            user = await self.user_crud.get_user_by_uuid(uuid, db)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except Exception as e:
            self.logger.error(f"Error retrieving user: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    async def update_user_route(
        self, uuid: str, user_data: UserCreate, db: AsyncSession = Depends(get_db)
    ) -> UserResponse:
        """
        Update a user by UUID.
        """
        try:
            updated_user = await self.user_crud.update_user(uuid, user_data, db)
            if not updated_user:
                raise HTTPException(status_code=404, detail="User not found or update failed")
            return updated_user
        except Exception as e:
            self.logger.error(f"Error updating user: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    async def delete_user_route(self, uuid: str, db: AsyncSession = Depends(get_db)) -> dict:
        """
        Delete a user by UUID.
        """
        try:
            deleted = await self.user_crud.delete_user(uuid, db)
            if not deleted:
                raise HTTPException(status_code=404, detail="User not found or deletion failed")
            return {"message": "User deleted successfully"}
        except Exception as e:
            self.logger.error(f"Error deleting user: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")


# Create an instance of the class and expose its router
user_routes = UserRoutes()
router = user_routes.router