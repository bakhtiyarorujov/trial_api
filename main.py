# main.py
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from typing import List#, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import or_


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class WrestlersBase(BaseModel):
    full_name: str


class TechniquesBase(BaseModel):
    name: str


class ActionsBase(BaseModel):
    name: str
    techniques: List[TechniquesBase]


class WrestsBase(BaseModel):
    wrestler_id: int
    opponent_id: int


class AuthorsBase(BaseModel):
    name: str


class StatusBase(BaseModel):
    name: str


class RecordsBase(BaseModel):
    second: str
    successful: bool
    score: int
    defense: bool
    flag: bool
    wrest_id: int
    technique_id: int
    author_id: int
    status_id: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#db_dependency = Annotated(Session, Depends(get_db))
        
@app.get('/{full_name}')
async def statistics(full_name: str, db: Session = Depends(get_db)):
    wrestler = db.query(models.Wrestlers).filter(models.Wrestlers.full_name == full_name).first()
    if wrestler is None:
        raise HTTPException(status_code=404, detail="Wrestler not found")
    
    protection_zone_count = db.query(models.Actions).join(models.Techniques).join(models.Records).filter(models.Records.wrest_id == wrestler.id, models.Actions.name == 'Protection zone').count()
    wrests_count = db.query(models.Wrests).filter(models.Wrests.wrestler_id == wrestler.id).count()
    try:
        result = protection_zone_count / wrests_count
    except ZeroDivisionError:
        result = 0.
    return {
        "Full name": full_name,
        "protection zone": result}