import sys
sys.path.append("..")

from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from starlette import status
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from models import Accounts
from database import SessionLocal
from pydantic import BaseModel, Field
from .auth import get_current_user

user_dependency = Annotated[dict,Depends(get_current_user)]


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
async def get_all_accounts(user: user_dependency, request: Request, db: db_dependency):

    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    accounts = db.query(Accounts).filter(Accounts.user_id == user.get('id'))
    return templates.TemplateResponse("accounts.html", {'request':request, 'accounts': accounts, 'user': user})


#BOOK---------
@router.get("/create_account", response_class=HTMLResponse)
async def create_account_landing(user: user_dependency, request: Request):
    
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("create_account.html",{'request': request, 'user': user})

@router.post("/create_account", response_class=HTMLResponse)
async def create_account(user: user_dependency, 
                        request: Request,
                        db: db_dependency,
                        account_id: int = Form(...),
                        nature: str = Form(...),
                        name: str = Form(...),
                        account_status: str = Form(...)):
    
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    if account_status == "Active":
        account_status = True
    else:
        account_status = False

    if db.query(Accounts).filter(Accounts.account_id == account_id).filter(Accounts.user_id == user.get('id')).first():
        return templates.TemplateResponse("create_account.html", {"request":request, "error_message": True, 'user': user})

    account_model = Accounts()
    account_model.account_id = account_id
    account_model.nature = nature
    account_model.name = name
    account_model.status = account_status
    account_model.user_id = user.get('id')

    db.add(account_model)
    db.commit()

    return RedirectResponse(url="/accounts", status_code=status.HTTP_302_FOUND)


#EDIT---------
@router.get("/edit_account/{account_id}", response_class=HTMLResponse)
async def edit_account_landing(user: user_dependency, request: Request, account_id: int, db: db_dependency):

    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    account = db.query(Accounts).filter(Accounts.account_id == account_id).filter(Accounts.user_id == user.get('id')).first()
    

    return templates.TemplateResponse("edit_account.html", {"request":request, "account": account, 'user': user})


@router.post("/edit_account/{account_id}", response_class=HTMLResponse)
async def edit_account(user: user_dependency, request: Request,
                        db: db_dependency,
                        account_id: int,
                        nature: str = Form(...),
                        name: str = Form(...),
                        account_status: str = Form(...)):

    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    if account_status == "Active":
        account_status = True
    else:
        account_status = False

    account_model = db.query(Accounts).filter(Accounts.account_id == account_id).filter(Accounts.user_id == user.get('id')).first()

    account_model.name = name
    account_model.nature = nature
    account_model.status = account_status

        
    db.add(account_model)
    db.commit()

    return RedirectResponse(url="/accounts", status_code=status.HTTP_302_FOUND)

#TODO: create HTMLresponse endpoint for delete
@router.delete("/delete_account/{account_id}", status_code=status.HTTP_201_CREATED)
async def delete_account(user: user_dependency, db: db_dependency, account_id: int):

    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)


    db.query(Accounts).filter(Accounts.account_id == account_id).delete()
    db.commit()