from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import sys
from .database import SessionLocal, engine
from . import crud, schemas, models
from typing import Optional, List

models.Base.metadata.create_all(bind=engine,checkfirst=True)

app = FastAPI()

## Poner filtro de si es true attachments o cambiar a true si le pongo uno o dejarlo a buen manejo del usuario?

# Por cada request que se hace crea una sesion y la cierra cuando termina
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FOLDERS
@app.get("/folders/", response_model=List[schemas.Folders])
def list_folders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    folders = crud.get_folders(db, skip=skip, limit=limit)
    return folders

## EMAILS
@app.post("/emails/", response_model=schemas.Email)
def read_email(to_name: str, froms_name: str, subject : str, db: Session = Depends(get_db)):
    # Chequeo que exista el emisor
    froms = crud.get_person(db, froms_name)
    if froms is None:
        raise HTTPException(status_code=404, detail="froms not found")
    # Chequeo que exista el receptor
    to = crud.get_person(db, to_name)
    if to is None:
        raise HTTPException(status_code=404, detail="to not found")
    # Chequeo que exista el mail
    db_email = crud.get_email_to_from_subject(db, to_name, froms_name, subject)
    if db_email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    return db_email

@app.post("/emails/create/", response_model=schemas.Email)
def create_email(email: schemas.EmailCreate, db: Session = Depends(get_db)):
    # Chequeo si ya existe el email_id
    email_dict = email.dict()
    db_email = crud.get_email(db,email_dict["id"])
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Creo el email Id
    db_email = crud.create_Email(db, email=email)
    return db_email

@app.delete("/delete_message/")
def delete_message(email_id: str, db: Session = Depends(get_db)):
    db_email = crud.get_email(db, email_id)
    if db_email:
        return crud.delete_message(db=db, email_id=email_id)
    else: 
        raise HTTPException(status_code=400, detail="Email not found")

## Attachments
@app.post("/emails/attachments/", response_model=schemas.Attachments)
def create_attachment_for_email(email_id: str, attachment: schemas.AttachmentCreate, db: Session = Depends(get_db)):
    return crud.create_email_attachment(db=db, attachment=attachment, email_id=email_id)

## Global

@app.post("/reset/")
def reset_data(db: Session = Depends(get_db)):
    crud.delete_all(db=db)
    crud.start_data(db)
    return "OK"





