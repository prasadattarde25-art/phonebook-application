from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .models import Contact
from .schemas import ContactCreate, ContactResponse


router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)


# --------------------------------------------------
# GET contacts - Search + Pagination
# --------------------------------------------------

@router.get("/")
def get_contacts(
    search: str | None = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    # Validate pagination parameters
    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="Page must be greater than 0"
        )

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100"
        )

    # Base query
    query = db.query(Contact)

    # Search
    if search:
        query = query.filter(
            Contact.name.ilike(f"%{search}%")
        )

    # Total records
    total = query.count()

    # Calculate offset
    offset = (page - 1) * limit

    # Get paginated contacts
    contacts = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    # Calculate total pages
    pages = (total + limit - 1) // limit

    return {
        "items": contacts,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": pages
    }


# --------------------------------------------------
# POST - Create contact
# --------------------------------------------------

@router.post("/", response_model=ContactResponse)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db)
):
    # Check duplicate phone
    existing_phone = db.query(Contact).filter(
        Contact.phone_number == contact.phone_number
    ).first()

    if existing_phone:
        raise HTTPException(
            status_code=400,
            detail="Phone number already exists"
        )

    # Check duplicate email
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


# --------------------------------------------------
# GET single contact
# --------------------------------------------------

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


# --------------------------------------------------
# PUT - Update contact
# --------------------------------------------------

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

    # Check duplicate phone
    existing_phone = db.query(Contact).filter(
        Contact.phone_number == updated_contact.phone_number,
        Contact.id != contact_id
    ).first()

    if existing_phone:
        raise HTTPException(
            status_code=400,
            detail="Phone number already exists"
        )

    # Check duplicate email
    if updated_contact.email:
        existing_email = db.query(Contact).filter(
            Contact.email == updated_contact.email,
            Contact.id != contact_id
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

    # Update fields
    contact.name = updated_contact.name
    contact.phone_number = updated_contact.phone_number
    contact.email = updated_contact.email
    contact.address = updated_contact.address

    db.commit()
    db.refresh(contact)

    return contact


# --------------------------------------------------
# DELETE - Delete contact
# --------------------------------------------------

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