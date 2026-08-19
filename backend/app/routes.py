from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .models import Contact
from .schemas import ContactCreate, ContactResponse


router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)


# GET all contacts
@router.get("/", response_model=list[ContactResponse])
def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contact).all()
    return contacts


# POST create a new contact
@router.post("/", response_model=ContactResponse)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db)
):
    existing_phone = db.query(Contact).filter(
        Contact.phone_number == contact.phone_number
    ).first()

    if existing_phone:
        raise HTTPException(
            status_code=400,
            detail="Phone number already exists"
        )

    if contact.email:
        existing_email = db.query(Contact).filter(
            Contact.email == contact.email
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

    new_contact = Contact(
        name=contact.name,
        phone_number=contact.phone_number,
        email=contact.email,
        address=contact.address
    )

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact


# GET one contact
@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db)
):
    contact = db.query(Contact).filter(
        Contact.id == contact_id
    ).first()

    if not contact:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    return contact


# PUT update contact
@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    updated_contact: ContactCreate,
    db: Session = Depends(get_db)
):
    contact = db.query(Contact).filter(
        Contact.id == contact_id
    ).first()

    if not contact:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    contact.name = updated_contact.name
    contact.phone_number = updated_contact.phone_number
    contact.email = updated_contact.email
    contact.address = updated_contact.address

    db.commit()
    db.refresh(contact)

    return contact

# DELETE contact
@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db)
):
    contact = db.query(Contact).filter(
        Contact.id == contact_id
    ).first()

    if not contact:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    db.delete(contact)
    db.commit()

    return {
        "message": "Contact deleted successfully"
    }