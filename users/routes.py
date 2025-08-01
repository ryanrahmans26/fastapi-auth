from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from users.schemas import CreateUserRequest
from users.services import create_user_account
from fastapi.responses import JSONResponse

router = APIRouter(
  prefix="/users",
  tags=["Users"],
  responses={404: {"description": "Not found"}},
)

@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):
  await create_user_account(data=data, db=db)
  payload = {"message": "User account has been creeated."}
  return JSONResponse(content=payload)
