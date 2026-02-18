"""Custom exceptions for email connector.

This module defines exception hierarchy for the email connector package.
All exceptions inherit from EmailConnectorError for easy catching.
"""


class EmailConnectorError(Exception):
    """Base exception for all email connector errors."""

    pass


class AuthenticationError(EmailConnectorError):
    """
    Raised when authentication fails.

    This includes invalid credentials, expired tokens,
    and failed token refresh attempts.
    """

    pass


class ConnectionError(EmailConnectorError):
    """
    Raised when connection to email provider fails.

    This includes network errors, API unavailability,
    and configuration errors.
    """

    pass


class NotFoundError(EmailConnectorError):
    """
    Raised when a requested resource does not exist.

    This includes non-existent messages, folders, or attachments.
    """

    pass


class RateLimitError(EmailConnectorError):
    """
    Raised when API rate limit is exceeded.

    Attributes
    ----------
    retry_after : int | None
        Seconds to wait before retrying, if provided by the API.
    """

    def __init__(self, message: str, retry_after: int | None = None):
        super().__init__(message)
        self.retry_after = retry_after


class PermissionError(EmailConnectorError):
    """
    Raised when the user lacks permission for an operation.

    This includes insufficient OAuth scopes or folder access restrictions.
    """

    pass
