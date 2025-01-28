#  app/routes/sms_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.schemas.schema import SMSCreate, SMSResponse
from app.curd_operation.sms_curd import create_sms, get_sms_by_uuid, get_all_sms, update_sms, delete_sms

router = APIRouter()

# Route to create a new SMS
@router.post("/sms/{user_uuid}", response_model=SMSResponse)
async def create_sms_route(sms: SMSCreate, db: AsyncSession = Depends(get_db)):
    return await create_sms(db=db, sms=sms)

# Route to get an SMS by UUID
@router.get("/sms/{user_uuid}", response_model=SMSResponse)
async def get_sms_route(uuid: str, db: AsyncSession = Depends(get_db)):
    sms = await get_sms_by_uuid(db=db, uuid=uuid)
    if sms is None:
        raise HTTPException(status_code=404, detail="SMS not found")
    return sms

# Route to get all SMS entries
@router.get("/sms/{user_uuid}", response_model=list[SMSResponse])
async def get_all_sms_route(db: AsyncSession = Depends(get_db)):
    sms_list = await get_all_sms(db=db)
    return sms_list

# Route to update an SMS entry by UUID
@router.put("/sms/{user_uuid}", response_model=SMSResponse)
async def update_sms_route(uuid: str, sms: SMSCreate, db: AsyncSession = Depends(get_db)):
    updated_sms = await update_sms(db=db, uuid=uuid, sms_data=sms)
    if updated_sms is None:
        raise HTTPException(status_code=404, detail="SMS not found")
    return updated_sms

# Route to delete an SMS entry by UUID
@router.delete("/sms/{uuid}", response_model=SMSResponse)
async def delete_sms_route(uuid: str, db: AsyncSession = Depends(get_db)):
    deleted_sms = await delete_sms(db=db, uuid=uuid)
    if deleted_sms is None:
        raise HTTPException(status_code=404, detail="SMS not found")
    return deleted_sms
