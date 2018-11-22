"""Custom exceptions."""

class Error(Exception):
    """Base exception class."""
    pass


class ParcelNotFoundError(Error):
    """Parcel was not found."""
    pass


class UserNotFoundError(Error):
    """User was not found."""
    pass


class IncorrectPasswordError(Error):
    """password is incorrect."""
    pass


class ApplicationError(Error):
    """the app just isn't working as it should."""
    pass
