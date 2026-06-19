from ..services.users_handling import check_user_exists



def filter_regulations_by_type(type: str, regulations: list[dict]) -> list[dict]:

    return [
        r for r in regulations if r["type"] == type
    ]


def filter_regulations_by_application(user_id: str, regulations: list[dict]) -> list[dict]:

    applicable_regulations = []
    user = check_user_exists(user_id)

    for r in regulations:

        match r["type"]:
            case "full-ban":
                if r["userCountryCode"] == user.country_code or r["userCountryCode"] == "*":
                    applicable_regulations.append(r)
            case "amount-based":
                user_stock_amount = next((s.quantity for s in user.stocks if s.ticker == r["stockSymbol"]), None)

                if user_stock_amount is not None and user_stock_amount > int(r["threshold"]):
                    applicable_regulations.append(r)

    return applicable_regulations
    


def filter_regulations_by_not_applying(user_id: str, regulations: list[dict]) -> list[dict]:

    not_applicable_regulations = []
    user = check_user_exists(user_id)

    for r in regulations:

        match r["type"]:
            case "full-ban":
                if r["userCountryCode"] != user.country_code and r["userCountryCode"] != "*":
                    not_applicable_regulations.append(r)

            case "amount-based":
                user_stock_amount = next((s.quantity for s in user.stocks if s.ticker == r["stockSymbol"]), None)

                if user_stock_amount is None or user_stock_amount <= int(r["threshold"]):
                    not_applicable_regulations.append(r)

    return not_applicable_regulations


        