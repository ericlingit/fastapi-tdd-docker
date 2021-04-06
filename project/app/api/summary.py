# In the tutorial, this file is named 'summaries.py'

"""This module interacts with http requests, while
the crud.py modle interacts with the database."""

from typing import List

from fastapi import APIRouter, HTTPException

from app.api import crud
from app.models.summary_payload import (SummaryPayloadSchema,
                                        SummaryResponseSchema)
from app.models.text_summary import SummarySchema

router = APIRouter()


@router.post("", response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema) -> SummaryResponseSchema:
    """Note in the decorator that the first arg is a blank string.
    In main.py, we added this endpoint with a prefix=/summary
    This means a POST request will run this function.
    If the decorator's first arg is "/xxx", then to run this
    function, the POST request need to go to /summary/xxx."""
    summary_id = await crud.post(payload)

    response = {"id": summary_id, "url": payload.url}
    return response


@router.get("/{id}", response_model=SummarySchema)
async def read_summary(id: int) -> SummarySchema:
    summary = await crud.get(id)

    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    return summary


@router.get("", response_model=List[SummarySchema])
async def read_all_summaries() -> List[SummarySchema]:
    return await crud.get_all()
