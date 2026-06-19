from .error_codes import ERRORS, ErrorSpec


class AppError(Exception):
    def __init__(self, code: str):
        try:
            self.spec: ErrorSpec = ERRORS[code]
        except KeyError:
            raise ValueError(f"Unknown error code: {code!r}") from None
        super().__init__(self.spec.message)
