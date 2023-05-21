import sys
sys.path.append("..")
import logging

logging.basicConfig(filename="C:\\Users\\facun\\Desktop\\PYTHON\\FastAPI\\accounts\\accountsApp\\logger.log", level=logging.INFO)
logger = logging.getLogger()

from fastapi import APIRouter, Depends, Path, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, Optional
from starlette import status
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from models import Ledgers, Accounts
from database import SessionLocal
from datetime import date
import json
from datetime import datetime
from .auth import get_current_user

router = APIRouter(
    prefix="/ledgers",
    tags=["ledgers"],
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
user_dependency = Annotated[dict,Depends(get_current_user)]

#TODO: quitar debits y credits. Dejar solo una variable con los datos económicos
#TODO: gestionar ledger_id para distintos usuarios


#LIST ALL-----
@router.get("/", response_class=HTMLResponse)
async def read_all_ledgers(user: user_dependency, request: Request, db: Session = Depends(get_db), date_filter: Optional[str] = None):

    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
       
    query = db.query(Ledgers).filter(Ledgers.user_id == user.get('id'))

    if date_filter:
        try:
            date_filter = datetime.strptime(date_filter, "%Y-%m-%d").date()
            query = query.filter(Ledgers.ledger_date == date_filter)
        except ValueError:
            # Handle invalid date format error here
            pass

    ledgers = query.all()

    #TODO: Change home.html to ledgers.html for all references to home.html
    return templates.TemplateResponse("home.html", {'request':request, 'ledgers': ledgers, 'user':user})


#BOOK---------
@router.get("/book_ledger", response_class=HTMLResponse)
async def create_ledger_landing(user: user_dependency, request: Request, db: Session = Depends(get_db)):
    
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("book_ledger.html",{'request': request, 'user':user})

@router.get("/fetch_accounts")
async def fetch_accounts(user: user_dependency, request: Request, db: Session = Depends(get_db)):
    
    if user is None:
        raise HTTPException(status_code=401, detail='Auth failed')
        
    accounts = db.query(Accounts).filter(Accounts.user_id == user.get("id"))
    
    accounts_dict = [account.name for account in accounts if account.status == True]
   
    return json.dumps(accounts_dict)


@router.post("/book_ledger", response_class=HTMLResponse)
async def create_ledger(user: user_dependency, 
                        db: Session = Depends(get_db),
                        description: str = Form(...),
                        ledger_date: date = Form(...),
                        table_data: str = Form(...)):

    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    data = json.loads(table_data)
    #shape: [{'account': 'Cash', 'amount':'20'}, {'account': 'Bank', 'amount':'-15'}, {'account': 'Debtors', 'amount':'-5'}]

    debits = []
    credits = []

    for row in data:
        account = row["account"]
        amount = float(row["amount"])

        if amount > 0:
            debits.append([account, amount])
        else:
            credits.append([account,-amount])

    ledger_model = Ledgers()
    ledger_model.description = description
    ledger_model.ledger_date = ledger_date
    ledger_model.debits = debits
    ledger_model.credits = credits
    ledger_model.user_id = user.get('id')

    db.add(ledger_model)
    db.commit()

    return RedirectResponse(url="/ledgers", status_code=status.HTTP_302_FOUND)


#EDIT---------
@router.get("/edit_ledger/{ledger_id}", response_class=HTMLResponse)
async def edit_ledger_landing(user: user_dependency, request: Request, ledger_id: int, db: Session = Depends(get_db)):

    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    accounts = db.query(Accounts).filter(Accounts.user_id == user.get('id'))
    accounts_dict = [account.name for account in accounts]

    ledger = db.query(Ledgers).filter(Ledgers.id == ledger_id).filter(Ledgers.user_id == user.get('id')).first()

    return templates.TemplateResponse("edit_ledger.html", {"request":request, "ledgers": ledger, 'accounts':accounts_dict, 'user': user})

#TODO: check if account is disabled to avoid using it when hitting edit ledger, cause the dropdown show display it anyways
@router.post("/edit_ledger/{ledger_id}", response_class=HTMLResponse)
async def edit_ledger(user: user_dependency,request: Request, ledger_id: int, db: Session = Depends(get_db),
                        description: str = Form(...),
                        ledger_date: date = Form(...),
                        table_data: str = Form(...)):


    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)


    ledger_model = db.query(Ledgers).filter(Ledgers.id == ledger_id).filter(Ledgers.user_id == user.get('id')).first()

    data = json.loads(table_data)

    debits = []
    credits = []

    for row in data:
        account = row["account"]
        amount = float(row["amount"])

        if amount > 0:
            debits.append([account, amount])
        else:
            credits.append([account,-amount])

    ledger_model.description = description
    ledger_model.ledger_date = ledger_date
    ledger_model.debits = debits
    ledger_model.credits = credits

    db.add(ledger_model)
    db.commit()

    return RedirectResponse(url="/ledgers", status_code=status.HTTP_302_FOUND)   



#DELETE-------
@router.get("/delete/{ledger_id}", response_class=HTMLResponse)
async def delete_ledger(user: user_dependency, db: Session = Depends(get_db), ledger_id: int = Path(gt=0)):

    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    ledger_model = db.query(Ledgers).filter(Ledgers.id == ledger_id).filter(Ledgers.user_id == user.get('id')).first()

    if ledger_model is None:
        raise RedirectResponse(url="/ledgers", status_code=status.HTTP_302_FOUND)

    db.query(Ledgers).filter(Ledgers.id == ledger_id).filter(Ledgers.user_id == user.get('id')).delete()
    db.commit()

    return RedirectResponse(url="/ledgers", status_code=status.HTTP_302_FOUND)



