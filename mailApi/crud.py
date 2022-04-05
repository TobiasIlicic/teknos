from sqlalchemy.orm import Session
import sys, os
import json
from . import models, schemas

# Email

def get_email_to_from_subject(db: Session, to_name: str, froms_name: str, subject: str):
    db_person_froms = get_person(db, froms_name)
    db_person_to = get_person(db, to_name)
    return db.query(models.Email).filter(models.Email.froms == db_person_froms).filter(models.Email.subject.startswith(subject)).filter(models.Email.to.contains(db_person_to)).first()

def get_email(db: Session, email_id: str):
    return db.query(models.Email).filter(models.Email.id == email_id).first()

def get_emails(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Email).offset(skip).limit(limit).all()

def create_Email(db: Session, email: schemas.EmailCreate):
    # Creo la persona que envia el email
    email_dict = email.dict()
    person_data = email_dict.pop('froms')
    db_Person = models.Person(**person_data)
    #Chequeo que la persona no este creada, y si no lo esta la creo
    #Poner nombre mas declarativo que db_Person2
    db_Person_exists = get_person(db, db_Person.name)
    if not db_Person_exists:
        db.add(db_Person)
        db.commit()
        db.refresh(db_Person)
    # Creo las personas que envian el email
    person_data = email_dict.pop('to')

    froms = get_person(db, db_Person.name)

    db_Email = models.Email(id = email.id,
                            subject = email.subject,
                            message = email.message,
                            time = email.time,
                            read = email.read,
                            starred = email.starred,
                            important = email.important,
                            hasAttachments = email.hasAttachments,
                            froms_id = froms.id
                            )
    
    for person in person_data:
        # Me fijo si la persona existe
        db_Person_exists = get_person(db, person['name'])
        #Si no existe la creo y la agrego
        if not db_Person_exists:
            person["avatar"] = ""
            db_Person = models.Person(**person)
            db_Email.to.append(db_Person)
        else:
            #Si existe la agrego
            db_Email.to.append(db_Person_exists)
    # Agrego el registro a la base de datos    
    db.add(db_Email)
    db.commit()
    db.refresh(db_Email)
    
    return db_Email


# Persons
def create_Person(db: Session, person: schemas.PersonCreate):
    db_Person = models.Person(email = person.email,
                            name = person.name,
                            avatar = person.avatar)
    db.add(db_Person)
    db.commit()
    db.refresh(db_Person)
    return db_Person

def get_persons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Person).offset(skip).limit(limit).all()

def get_person(db: Session, person_name: str):
    return db.query(models.Person).filter(models.Person.name == person_name).first()


#Attachments
def get_attachments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Attachments).offset(skip).limit(limit).all()

def get_attachments_email_id(db: Session, email_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Attachments).filter(models.Attachments.email_id==email_id).all()


def create_email_attachment(db: Session, attachment: schemas.AttachmentCreate, email_id: str):
    db_attachment = models.Attachments(type=attachment.type,
                                        fileName=attachment.fileName,
                                        preview=attachment.preview,
                                        url=attachment.url,
                                        size=attachment.size,
                                        email_id=email_id)
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment

def delete_message(db: Session, email_id: str):
    db_attachments = get_attachments_email_id(db=db, email_id=email_id)
    # Borro todos los attachments
    for attachment in db_attachments:
        db.delete(attachment)
        db.commit()
    # Borro todos los emails
    db_email = get_email(db=db,email_id=email_id)
    db.delete(db_email)
    db.commit()
    return "delete succesful"

# Folders

def create_folder(db: Session, folder: schemas.FolderCreate):
    db_folder = models.Folder(name = folder.name,
                                title = folder.title,
                                icon = folder.icon)
    db.add(db_folder)
    db.commit()
    return db_folder

def get_folders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Folder).offset(skip).limit(limit).all()


# Globales

def start_data(db: Session):
    # Cargo las carpetas
    script_folders = os.path.abspath(r"Modelos\folders.json")
    with open(script_folders) as f:
        #lo transformo en un json
        data = json.load(f)
        for folder_dict in data["data"]:
            folder = schemas.FolderCreate(**folder_dict)
            db_folder = create_folder(db, folder)
            db.add(db_folder)
            db.commit()
        f.close()

    # Todos los archivos para cargar data
    script_list = [r"Modelos\inbox.json", r"Modelos\important.json",
                    r"Modelos\sent.json", r"Modelos\spam.json",
                     r"Modelos\starred.json", r"Modelos\trash.json"]
    for script in script_list:
        #Consigo el path absoluto del archivo
        script_dir = os.path.abspath(script)
        with open(script_dir) as f:
            #lo transformo en un json
            data = json.load(f)
            #Itero por todos los emails
            for email_dict in data["data"]:
                #Saco los attachments del email si es que hay
                attachments = email_dict.get("attachments")
                if(attachments == ""):
                    attachments = email_dict.pop("attachments")
                #Creo el email
                email = schemas.EmailCreate(**email_dict)
                db_email = create_Email(db, email)
                db.add(db_email)
                db.commit()
                email_id = db_email.id
                #Creo los attachments
                if not (attachments == None):
                    #aca quiero insertar los attachments
                    for attachment in attachments:
                        db_attachment = schemas.AttachmentCreate(**attachment)
                        create_email_attachment(db,db_attachment,email_id)
            f.close()



def delete_all(db: Session):
    db_attachments = get_attachments(db=db)
    # Borro todos los attachments
    for attachment in db_attachments:
        db.delete(attachment)
        db.commit()
    # Borro todos los emails
    db_emails = get_emails(db=db)
    for email in db_emails:
        db.delete(email)
        db.commit()
    db_persons = get_persons(db)
    # Borro todas las personas
    for person in db_persons:
        db.delete(person)
        db.commit()
    #Borro todas las carpetas
    db_folders = get_folders(db)
    for folder in db_folders:
        db.delete(folder)
        db.commit()
    return