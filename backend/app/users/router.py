from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.dependencies import get_db
from app.users import service
from app.users.schema import (
    UserCreate,
    UserResponse,
    UserUpdate,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    password_hash = hash_password(user.password)

    return service.create_user(
        db,
        user,
        password_hash,
    )


@router.get(
    "",
    response_model=list[UserResponse],
)
def get_users(
    db: Session = Depends(get_db),
):
    return service.get_all_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    return service.get_user_by_id(
        db,
        user_id,
    )


@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    updated_data: UserUpdate,
    db: Session = Depends(get_db),
):
    user = service.get_user_by_id(
        db,
        user_id,
    )

    return service.update_user(
        db,
        user,
        updated_data,
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = service.get_user_by_id(
        db,
        user_id,
    )

    service.delete_user(
        db,
        user,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )