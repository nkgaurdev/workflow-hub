from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.users.model import User
from app.users.schema import UserCreate, UserUpdate


def create_user(
    db: Session,
    user: UserCreate,
    password_hash: str,
) -> User:
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        password_hash=password_hash,
        role=user.role,
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists.",
        )


def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


def get_user_by_id(
    db: Session,
    user_id: int,
) -> User:
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    return db.query(User).filter(User.email == email).first()


def update_user(
    db: Session,
    user: User,
    updated_data: UserUpdate,
) -> User:
    user.full_name = updated_data.full_name
    user.role = updated_data.role
    user.is_active = updated_data.is_active

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user: User,
) -> None:
    db.delete(user)
    db.commit()