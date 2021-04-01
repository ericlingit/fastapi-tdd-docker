# In the tutorial, this file is named 'summaries.py'

'''This module interacts with http requests, while
the crud.py modle interacts with the database.'''

from fastapi import APIRouter, HTTPException

from app.api import crud
from app.models.summary_payload import SummaryPayloadSchema, SummaryResponseSchema


router = APIRouter()


@router.post('', response_model=SummaryResponseSchema, status_code=201)
async def create_summary(payload: SummaryPayloadSchema) -> SummaryResponseSchema:
    '''Note in the decorator that the first arg is a blank string.
    In main.py, we added this endpoint with a prefix=/summary
    This means a POST request will run this function.
    If the decorator's first arg is "/xxx", then to run this
    function, the POST request need to go to /summary/xxx.'''
    summary_id = await crud.post(payload)

    response = {
        'id': summary_id,
        'url': payload.url
    }
    return response
