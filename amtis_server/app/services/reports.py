from ..models.reports import ReportStockTransactionsQuery, ReportTransactionsQuery
from ..db.store import db
from datetime import datetime, date
from ..adapters.market import market

def datetime_within_range(current_datetime: datetime, start_date: date|None, end_date: date|None) -> bool:
    current = current_datetime.date()

    if end_date is None and start_date is None:
        return True
    
    if start_date is None:
        assert end_date is not None
        return current <= end_date
        
    if end_date is None:
        assert start_date is not None
        return current >= start_date
    
    
    return start_date <= current <= end_date


def format_stock_transactions_report(report_specs: ReportStockTransactionsQuery, user_id: str) -> list[dict]:
    result = []

    for t in db["users"][user_id].transactions:
        if (t.get("ticker") is not None
            and datetime_within_range(datetime.fromisoformat(t["timestamp"]), report_specs.startDate, report_specs.endDate)
            and (report_specs.stock_type == t["type"] or report_specs.stock_type is None)
            and t["currency"] == "USD"):

            result.append({
                "type": t["type"],
                "ticker": t["ticker"],
                "countryCode": t["countryCode"],
                "quantity": t["quantity"],
                "price": float(t["price"]),
                "total": float(t["quantity"] * t["price"]),
                "timestamp": t["timestamp"].replace("+00:00", "Z")
            })

    return result


def format_transactions_report(report_specs: ReportTransactionsQuery, user_id: str) -> list[dict]:
    result = []

    for t in db["users"][user_id].transactions:
        item_type = "stock" if t.get("ticker") is not None else "currency"

        if (datetime_within_range(datetime.fromisoformat(t["timestamp"]), report_specs.startDate, report_specs.endDate)
            and (item_type == report_specs.item_type or report_specs.item_type is None)
            and (report_specs.stock_type is None or report_specs.item_type != "stock" or report_specs.stock_type == t["type"])
            ):

            if item_type == "stock":
                result.append({
                    "itemType": "stock",
                    "type": t["type"],
                    "ticker": t["ticker"],
                    "countryCode": t["countryCode"],
                    "currency": t["currency"],
                    "quantity": t["quantity"],
                    "price": float(t["price"]),
                    "total": float(t["quantity"] * t["price"]),
                    "timestamp": t["timestamp"].replace("+00:00", "Z")
                })
            
            else:
                result.append({
                    "itemType": "currency",
                    "type": "exchange",
                    "from": t["from"],
                    "to": t["to"],
                    "amount": t["amount"],
                    "result": t["result"],
                    "timestamp": t["timestamp"].replace("+00:00", "Z")
                })

    return result