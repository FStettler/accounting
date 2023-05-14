import sys
sys.path.append("..")

from fastapi import APIRouter, Depends, Query, Path, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, Optional
from starlette import status
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from models import Accounts
from database import SessionLocal
from pydantic import BaseModel, Field
from datetime import date
import json


router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={404: {"description": "Not found"}}
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory="templates")

db_dependency = Annotated[Session, Depends(get_db)]

class AccountRequest(BaseModel):
    id: int = Field(gt=99, lt=1000)
    name: str = Field(min_length=3, max_length=20)
    nature: str
    status: bool


#LIST ALL-----

@router.get("/", response_class=HTMLResponse)
async def get_all_accounts(request: Request, db: db_dependency):
    accounts = db.query(Accounts).all()

    return templates.TemplateResponse("accounts.html", {'request':request, 'accounts': accounts})


#BOOK---------
@router.get("/create_account", response_class=HTMLResponse)
async def create_account_landing(request: Request):
    return templates.TemplateResponse("create_account.html",{'request': request})

@router.post("/create_account", response_class=HTMLResponse)
async def create_account(request: Request,
                        db: db_dependency,
                        account_id: int = Form(...),
                        nature: str = Form(...),
                        name: str = Form(...),
                        account_status: str = Form(...)):

    if account_status == "Active":
        account_status = True
    else:
        account_status = False

    if db.query(Accounts).filter(Accounts.id == account_id).first():
        return templates.TemplateResponse("create_account.html", {"request":request, "error_message": True})

    account_model = Accounts()
    account_model.id = account_id
    account_model.nature = nature
    account_model.name = name
    account_model.status = account_status

    db.add(account_model)
    db.commit()

    return RedirectResponse(url="/accounts", status_code=status.HTTP_302_FOUND)


#EDIT---------
@router.get("/edit_account/{account_id}", response_class=HTMLResponse)
async def edit_account_landing(request: Request, account_id: int, db: db_dependency):
    
    account = db.query(Accounts).filter(Accounts.id == account_id).first()

    return templates.TemplateResponse("edit_account.html", {"request":request, "account": account})


@router.post("/edit_account/{account_id}", response_class=HTMLResponse)
async def edit_account(request: Request,
                        db: db_dependency,
                        account_id: int,
                        nature: str = Form(...),
                        name: str = Form(...),
                        account_status: str = Form(...)):
    
    if account_status == "Active":
        account_status = True
    else:
        account_status = False

    account_model = db.query(Accounts).filter(Accounts.id == account_id).first()

    account_model.name = name
    account_model.nature = nature
    account_model.status = account_status
        
    db.add(account_model)
    db.commit()

    return RedirectResponse(url="/accounts", status_code=status.HTTP_302_FOUND)














@router.put("/edit_account/{account_id}", status_code=status.HTTP_201_CREATED)
async def create_account(db: db_dependency, account_request: AccountRequest, account_id: int):

    account_model = db.query(Accounts).filter(Accounts.id == account_id).first()

    account_model.id = account_request.id
    account_model.name = account_request.name
    account_model.nature = account_request.nature
    account_model.status = account_request.status
        
    db.add(account_model)
    db.commit()

@router.delete("/delete_account/{account_id}", status_code=status.HTTP_201_CREATED)
async def delete_account(db: db_dependency, account_id: int):
    

    db.query(Accounts).filter(Accounts.id == account_id).delete()
    db.commit()