from fastapi import APIRouter, Query, Depends
from typing import Annotated
from ..models.regulations import RegulationFilterQuery
from ..services.regulations import filter_regulations_by_type, filter_regulations_by_application, filter_regulations_by_not_applying
from ..adapters.market import market
from ..dependencies.cookies import get_user_id


router = APIRouter()

@router.get("/api/regulations")
def show_related_regulations(
    filter_query: Annotated[RegulationFilterQuery, Query()],
    user_id: Annotated[str, Depends(get_user_id)]
):
    
    regulations = market.get_market_regulations()["regulations"]

    if filter_query.type is not None:
        regulations = filter_regulations_by_type(filter_query.type, regulations)

    if filter_query.is_applicable_to_me:
        regulations = filter_regulations_by_application(user_id, regulations)

    elif filter_query.is_applicable_to_me == False:
        regulations = filter_regulations_by_not_applying(user_id, regulations)

    return {"regulations": regulations}