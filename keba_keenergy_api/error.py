"""KEBA KeEnergy API error classes."""


class APIError(Exception):
    """API Error."""


class InvalidJsonError(APIError):
    """Invalid JSON Data Error."""
