from fastapi import APIRouter, Depends
from typing import Annotated
from ..dependencies.cookies import get_user_id
from ..db.store import db
from ..models.user import UserBalance
from ..models.transaction import TransactionInfo, TransactionInfoMultiCurr
from ..services.transactions_handling import deposit_money, withdraw_money
from decimal import Decimal
from ..errors.exceptions import AppError
from ..errors.error_codes import Codes


router = APIRouter()


@router.get("/api/users/me/wallet")
def get_wallet_balance_usd(
    user_id: Annotated[str, Depends(get_user_id)]
):

    amount_in_dollars: Decimal = next((b.amount for b in db["users"][user_id].balances if b.currency == "USD"), Decimal(0))
    return {
        "balance": amount_in_dollars
    }


@router.post("/api/users/me/wallet/deposits", status_code=201)
def deposit_money_in_wallet(
    deposit_info: TransactionInfo,
    user_id: Annotated[str, Depends(get_user_id)]
):
    deposit_money(user_id, deposit_info.amount)

    return get_wallet_balance_usd(user_id=user_id)


@router.post("/api/users/me/wallet/withdrawals", status_code=201)
def withdraw_money_from_wallet(
    withdraw_info: TransactionInfo,
    user_id: Annotated[str, Depends(get_user_id)]
):
    withdraw_money(user_id, withdraw_info.amount)

    return get_wallet_balance_usd(user_id=user_id)


@router.get("/api/v2/wallet")
def get_wallet_balance_multicurr(
    user_id: Annotated[str, Depends(get_user_id)]
):

    return {
        "balances": [{
            "currency": b.currency,
            "amount": b.amount
        } for b in db["users"][user_id].balances]
    }


@router.get("/api/v2/wallet/{currency}")
def get_wallet_in_currency(
    user_id: Annotated[str, Depends(get_user_id)],
    currency: str
):
    if not currency.isalpha():
        raise AppError(Codes.INVALID_FORMAT)

    balance: UserBalance|None = next((b for b in db["users"][user_id].balances if b.currency == currency), None)

    if balance is None:
        raise AppError(Codes.NOT_FOUND)

    return {
        "currency": balance.currency,
        "amount": balance.amount
    }


@router.post("/api/v2/wallet/deposits", status_code=201)
def deposit_money_in_wallet_multicurr(
    deposit_info: TransactionInfoMultiCurr,
    user_id: Annotated[str, Depends(get_user_id)]
):
    deposit_money(user_id, deposit_info.amount, currency=deposit_info.currency)

    balance_in_currency = next(b for b in db["users"][user_id].balances if b.currency == deposit_info.currency) # impossible for the currency not to exist

    return {
        "currency": balance_in_currency.currency,
        "newBalance": balance_in_currency.amount
    }


@router.post("/api/v2/wallet/withdrawals", status_code=201)
def withdraw_money_from_wallet_multicurr(
    deposit_info: TransactionInfoMultiCurr,
    user_id: Annotated[str, Depends(get_user_id)]
):
    withdraw_money(user_id, deposit_info.amount, currency=deposit_info.currency)

    balance_in_currency = next(b for b in db["users"][user_id].balances if b.currency == deposit_info.currency) # impossible for the currency not to exist

    return {
        "currency": balance_in_currency.currency,
        "newBalance": balance_in_currency.amount
    }