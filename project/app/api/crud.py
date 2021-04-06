'''This module interacts with the database through
`app.models.text_summary.TextSummary` class.

Why not merge this module with summary.py?
My guess is that this makes testing easier...?
'''

from app.models.summary_payload import SummaryPayloadSchema, SummaryResponseSchema
from app.models.text_summary import TextSummary


async def post(payload: SummaryPayloadSchema) -> int:
    summary = TextSummary(
        url=payload.url,
        summary='test summary'
    )

    await summary.save()
    return summary.id