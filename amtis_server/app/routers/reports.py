from fastapi import Query, APIRouter, Depends
from typing import Annotated
from ..models.reports import ReportStockTransactionsQuery, ReportTransactionsQuery
from ..services.reports import format_stock_transactions_report, format_transactions_report
from ..dependencies.cookies import get_user_id

router = APIRouter()

@router.get("/api/reports/history")
def get_stock_transactions_history(
    report_params: Annotated[ReportStockTransactionsQuery, Query()],
    user_id: str = Depends(get_user_id),
):
    result = format_stock_transactions_report(report_params, user_id)
    return {
        "startDate": report_params.startDate,
        "endDate": report_params.endDate,
        "items": result 
    }


@router.get("/api/v2/reports/history")
def get_all_transactions_history(
    report_params: Annotated[ReportTransactionsQuery, Query()],
    user_id: str = Depends(get_user_id),
):
    result = format_transactions_report(report_params, user_id)

    return {
        "startDate": report_params.startDate,
        "endDate": report_params.endDate,
        "items": result 
    }