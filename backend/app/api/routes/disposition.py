from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List

from api.models.disposition import DispositionCreate, DispositionRead, DispositionUpdate
from db.database import get_db
from db.schemas.disposition import Disposition


router = APIRouter()


#
# CREATE
#


@router.post(
    "/disposition",
    tags=["disposition"],
    response_model=bool,
    responses={
        status.HTTP_201_CREATED: {
            "headers": {
                "Location": {"description": "The path to retrieve the disposition"},
            },
        },
        status.HTTP_409_CONFLICT: {"description": "A disposition with this rank or value already exists"},
    },
    status_code=status.HTTP_201_CREATED,
)
def create_disposition(
    disposition: DispositionCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    new_disposition = Disposition(**disposition.dict())
    db.add(new_disposition)

    try:
        db.commit()
        response.headers["Location"] = request.url_for("get_disposition", id=new_disposition.id)
        return True
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Disposition with rank {disposition.rank} or value {disposition.value} already exists"
        )


#
# READ
#


@router.get(
    "/disposition",
    tags=["disposition"],
    response_model=List[DispositionRead],
)
def get_all_dispositions(db: Session = Depends(get_db)):
    return db.execute(select(Disposition)).scalars().all()


@router.get(
    "/disposition/{id}",
    tags=["disposition"],
    response_model=DispositionRead,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "The disposition ID was not found"},
    },
)
def get_disposition(id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Disposition).where(Disposition.id == id)).scalars().one_or_none()

    if result is None:
        raise HTTPException(status_code=404, detail=f"Disposition ID {id} does not exist.")

    return result


#
# UPDATE
#


@router.put(
    "/disposition/{id}",
    tags=["disposition"],
    response_model=bool,
    responses={
        status.HTTP_200_OK: {
            "headers": {
                "Location": {"description": "The path to retrieve the disposition"}
            },
        },
        status.HTTP_400_BAD_REQUEST: {"description": "The database returned an IntegrityError"},
        status.HTTP_404_NOT_FOUND: {"description": "The disposition ID was not found"},
    },
)
def update_disposition(
    id: int,
    disposition: DispositionUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # True to perform the update
    try:
        result = db.execute(
            update(Disposition)
            .where(
                Disposition.id == id
            ).values(
                # exclude_unset is needed for update routes so that any values in the Pydantic model
                # that are not being updated are not set to None. Instead they will be removed from the dict.
                **disposition.dict(exclude_unset=True)
            )
        )

        # Verify a row was actually updated
        if result.rowcount != 1:
            raise HTTPException(status_code=404, detail=f"Disposition ID {id} does not exist.")

        # Set the Location header to get the disposition
        response.headers["Location"] = request.url_for("get_disposition", id=id)
        return True
    # An IntegrityError will happen if the rank or value already exists or was set to None
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Got an IntegrityError while updating disposition ID {id}.")


#
# DELETE
#


@router.delete(
    "/disposition/{id}",
    tags=["disposition"],
    response_model=bool,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Unable to delete the disposition"},
    },
)
def delete_disposition(id: int, db: Session = Depends(get_db)):
    # NOTE: This will need to be updated to account for foreign key constraint errors when Alert endpoints exist.
    result = db.execute(delete(Disposition).where(Disposition.id == id))

    if result.rowcount != 1:
        raise HTTPException(status_code=400, detail=f"Unable to delete disposition ID {id} or it does not exist.")

    return True