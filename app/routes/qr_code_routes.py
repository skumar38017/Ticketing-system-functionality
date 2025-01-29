#  app/routes/qr_code_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.schemas.schema import QRCodeCreate, QRCodeResponse
from app.curd_operation.qr_code_curd import create_qr_code, get_qr_code_by_uuid, get_qr_codes_by_user_uuid, update_qr_code, delete_qr_code

router = APIRouter()

# Route to create a new QR code
@router.post("/qr-codes/{user_uuid}", response_model=QRCodeResponse)
async def create_qr_code_route(qr_code: QRCodeCreate, db: AsyncSession = Depends(get_db)):
    return await create_qr_code(db=db, qr_code=qr_code)

# Route to get a QR code by UUID
@router.get("/qr-codes/{uuid}", response_model=QRCodeResponse)
async def get_qr_code_route(uuid: str, db: AsyncSession = Depends(get_db)):
    qr_code = await get_qr_code_by_uuid(db=db, uuid=uuid)
    if qr_code is None:
        raise HTTPException(status_code=404, detail="QR code not found")
    return qr_code

# Route to get all QR codes for a user
@router.get("/qr-codes/{user_uuid}", response_model=list[QRCodeResponse])
async def get_qr_codes_by_user_route(user_uuid: str, db: AsyncSession = Depends(get_db)):
    qr_codes = await get_qr_codes_by_user_uuid(db=db, user_uuid=user_uuid)
    return qr_codes

# Route to update a QR code
@router.put("/qr-codes/{user_uuid}", response_model=QRCodeResponse)
async def update_qr_code_route(uuid: str, qr_code: QRCodeCreate, db: AsyncSession = Depends(get_db)):
    updated_qr_code = await update_qr_code(db=db, uuid=uuid, qr_code_data=qr_code)
    if updated_qr_code is None:
        raise HTTPException(status_code=404, detail="QR code not found")
    return updated_qr_code

# Route to delete a QR code by UUID
@router.delete("/qr-codes/{user_uuid}", response_model=QRCodeResponse)
async def delete_qr_code_route(uuid: str, db: AsyncSession = Depends(get_db)):
    deleted_qr_code = await delete_qr_code(db=db, uuid=uuid)
    if deleted_qr_code is None:
        raise HTTPException(status_code=404, detail="QR code not found")
    return deleted_qr_code
