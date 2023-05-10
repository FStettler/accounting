import sys
sys.path.append("..")

from fastapi import APIRouter, Depends, HTTPException, Path, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
from starlette import status
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from models import Ledgers
from database import SessionLocal
from pydantic import BaseModel, Field
from datetime import date
import json

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

#TODO: quitar debits y credits. Dejar solo una variable con los datos económicos
class LedgerRequest(BaseModel):
    description: str = Field(min_length=3, max_length=50)
    ledger_date: date
    debits: dict
    credits: dict

#LIST ALL-----
@router.get("/", response_class=HTMLResponse)
async def read_all_ledgers(request: Request, db: Session = Depends(get_db)):

    ledgers = db.query(Ledgers).all()

    return templates.TemplateResponse("home.html", {'request':request, 'ledgers': ledgers})



#BOOK---------
@router.get("/book_ledger", response_class=HTMLResponse)
async def create_ledger_landing(request: Request):
    return templates.TemplateResponse("book_ledger.html",{'request': request})

@router.post("/book_ledger", response_class=HTMLResponse)
async def create_ledger(request: Request,
                        db: Session = Depends(get_db),
                        description: str = Form(...),
                        ledger_date: date = Form(...),
                        table_data: str = Form(...)):

    data = json.loads(table_data)

    #TODO: el botón de add line y delete line ejecutan el submit. Evitar que eso suceda

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

    db.add(ledger_model)
    db.commit()

    return RedirectResponse(url="/ledgers", status_code=status.HTTP_302_FOUND)



#EDIT---------
@router.get("/edit_ledger/{ledger_id}", response_class=HTMLResponse)
async def edit_ledger(request: Request, ledger_id: int, db: Session = Depends(get_db)):
    
    ledger = db.query(Ledgers).filter(Ledgers.id == ledger_id).first()

    return templates.TemplateResponse("edit_ledger.html", {"request":request, "ledgers": ledger})

@router.post("/edit_ledger/{ledger_id}", response_class=HTMLResponse)
async def edit_ledger(request: Request, ledger_id: int, db: Session = Depends(get_db),
                        description: str = Form(...),
                        ledger_date: date = Form(...),
                        table_data: str = Form(...)):
    
    ledger_model = db.query(Ledgers).filter(Ledgers.id == ledger_id).first()

    data = json.loads(table_data)

    #TODO: el botón de add line y delete line ejecutan el submit. Evitar que eso suceda

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
async def delete_ledger(db: Session = Depends(get_db), ledger_id: int = Path(gt=0)):
    
    ledger_model = db.query(Ledgers).filter(Ledgers.id == ledger_id).first()

    if ledger_model is None:
        raise RedirectResponse(url="/ledgers", status_code=status.HTTP_302_FOUND)

    db.query(Ledgers).filter(Ledgers.id == ledger_id).delete()
    db.commit()

    return RedirectResponse(url="/ledgers", status_code=status.HTTP_302_FOUND)



