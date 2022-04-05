from pydantic import BaseModel
import sys
from typing import Optional, List

from .models import Attachments, Person

## FOLDERS
class FolderBase(BaseModel):
    name: str
    title: str
    icon: str

class FolderCreate(FolderBase):
    pass

class Folders(FolderBase):
    id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

## PERSONS

class PersonBase(BaseModel):
    email: str
    name: str

class PersonCreate(PersonBase):
    avatar: str
    pass

class Persons(PersonBase):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class To(PersonBase):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class Froms(PersonBase):
    avatar: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


## ATTACHMENTS

class AttachmentBase(BaseModel):
    type: str
    fileName: str
    preview: str
    url: str
    size: str


class AttachmentCreate(AttachmentBase):
    pass

class Attachments(AttachmentBase):
    id: int
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


### EMAIL

class EmailBase(BaseModel):
    id: str
    subject: str
    message: str
    time: str
    read: bool
    starred: bool
    important: bool
    hasAttachments: bool 

class EmailCreate(EmailBase):
    froms: Froms
    to: List[To] 
    pass

class Email(EmailBase):
    froms: Froms
    to: List[To] 
    attachments: List[Attachments] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
