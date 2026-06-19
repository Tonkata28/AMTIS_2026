from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorSpec:
    code: str
    message: str
    status: int

    
ERRORS: dict[str, ErrorSpec] = {
    "INVALID_REQUEST": ErrorSpec(
        "INVALID_REQUEST", "Невалидна заявка", 400),

    # ─── Data validation ──────────────────────────────
    "MISSING_REQUIRED_FIELDS": ErrorSpec(
        "MISSING_REQUIRED_FIELDS", "Липсват задължителни полета", 400),
    "VALIDATION_FAILED": ErrorSpec(
        "VALIDATION_FAILED", "Валидацията е неуспешна", 400),
    "INVALID_VALUE": ErrorSpec(
        "INVALID_VALUE", "Невалидна стойност", 400),
    "INVALID_FORMAT": ErrorSpec(
        "INVALID_FORMAT", "Невалиден формат на данните", 400),
    "DUPLICATE_REQUEST": ErrorSpec(
        "DUPLICATE_REQUEST", "Дублирана заявка", 409
    ),
    "CONFLICT": ErrorSpec(
        "CONFLICT", "Конфликт в заявката", 409
    ),
    "UNSUPPORTED_FORMAT": ErrorSpec(
        "UNSUPPORTED_FORMAT", "Неподдържан формат", 406 # should be 415, but expects 406, so possible issue
    ),
    "AUTH_REQUIRED": ErrorSpec(
        "AUTH_REQUIRED", "Необходима е автентикация", 401
    ),
    "INVALID_CREDENTIALS": ErrorSpec(
        "INVALID_CREDENTIALS", "Невалидни идентификационни данни", 401
    ),
    "INSUFFICIENT_FUNDS": ErrorSpec(
        "INSUFFICIENT_FUNDS", "Недостатъчна наличност", 402
    ),
    "INSUFFICIENT_QUANTITY": ErrorSpec(
        "INSUFFICIENT_QUANTITY", "Недостатъчно количество", 400
    ),
    "NOT_FOUND": ErrorSpec(
        "NOT_FOUND", "Ресурсът не е намерен", 404
    ),
    "REGULATION_BLOCKED": ErrorSpec(
        "REGULATION_BLOCKED", "Операцията е блокирана от регулация", 451
    ),

    "INTERNAL_ERROR": ErrorSpec(
        "INTERNAL_ERROR", "Възникна грешка при изпълнение", 500
    )
}

class Codes:
    INVALID_REQUEST = "INVALID_REQUEST" # generic code for not specified issues

    MISSING_REQUIRED_FIELDS = "MISSING_REQUIRED_FIELDS"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    INVALID_FORMAT = "INVALID_FORMAT"
    INVALID_VALUE = "INVALID_VALUE"
    DUPLICATE_REQUEST = "DUPLICATE_REQUEST"
    CONFLICT = "CONFLICT"
    UNSUPPORTED_FORMAT = "UNSUPPORTED_FORMAT"
    AUTH_REQUIRED = "AUTH_REQUIRED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    INSUFFICIENT_QUANTITY = "INSUFFICIENT_QUANTITY"
    NOT_FOUND = "NOT_FOUND"
    REGULATION_BLOCKED = "REGULATION_BLOCKED"

    INTERNAL_ERROR = "INTERNAL_ERROR"