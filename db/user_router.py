from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
import data_schema, data_crud
from data_table import User

router = APIRouter(
    prefix="/api/user",
)

#https://github.com/pahkey/fastapi-book/blob/master/domain/answer/answer_router.py
