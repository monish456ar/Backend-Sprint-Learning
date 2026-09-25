class CountryError(Exception):
    """Base class for all country‑related errors."""
    pass

class UnknownCountryCodeError(CountryError):
    def __init__(self, code: str):
        super().__init__(f"Unknown country code '{code}'.")

class UnsupportedSortFieldError(CountryError):
    def __init__(self, field: str):
        super().__init__(f"Unsupported sort field '{field}'. Use 'population' or 'area'.")

class InvalidQueryParameterError(CountryError):
    def __init__(self, message: str):
        super().__init__(message)
