import sys
sys.path.append("..")

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
    prefix="/trial_balance",
    tags=["trial_balance"],
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


@router.get("/", response_class=HTMLResponse)
async def trial_balance_by_period(user: user_dependency, request: Request, db: db_dependency, date_filter: Optional[str] = None):
    
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND) 
    
    query = db.query(Ledgers).filter(Ledgers.user_id == user.get('id'))

    if date_filter:
        try:
            date_filter = datetime.strptime(date_filter, "%Y-%m-%d").date()
            query = query.filter(Ledgers.ledger_date == date_filter)
        except ValueError:
            pass
    
    trial_balance = {}
    
    for ledger in query:
        for debits in ledger.debits:
            try:
                trial_balance[debits[0]] += debits[1]
            except:
                trial_balance[debits[0]] = debits[1]
        
        for credits in ledger.credits:
            try:
                trial_balance[credits[0]] += credits[1] * -1
            except:
                trial_balance[credits[0]] = credits[1] * -1


    return templates.TemplateResponse("trial_balance.html", {'request':request, 'trial_balance': trial_balance, 'user':user})
