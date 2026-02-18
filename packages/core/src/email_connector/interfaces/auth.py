"""Authentication provider interface for email services.

This module defines the abstract base class for authentication providers.
Each email provider (Outlook, Gmail, etc.) should implement this interface.
"""

from abc import ABC, abstractmethod


class EmailAuthProvider(ABC):
    """
    Abstract authentication provider for email services.

    This interface defines the contract for authentication providers.
    Implementations handle provider-specific authentication flows
    (OAuth2, API keys, etc.) while exposing a uniform interface.

    Examples
    --------
    >>> auth = MSGraphAuthProvider(client_id="...", tenant_id="...")
    >>> if auth.authenticate():
    ...     token = auth.get_access_token()
    ...     # Use token for API calls
    """

    @abstractmethod
    def authenticate(self) -> bool:
        """
        Perform authentication flow.

        This method initiates the authentication process, which may involve
        user interaction (e.g., browser-based OAuth flow) or automated
        token retrieval (e.g., client credentials flow).

        Returns
        -------
        bool
            True if authentication was successful, False otherwise.

        Raises
        ------
        AuthenticationError
            If authentication fails due to invalid credentials or
            configuration errors.
        """
        pass

    @abstractmethod
    def get_access_token(self) -> str:
        """
        Return current valid access token.

        This method should handle token refresh if the current token
        is expired or about to expire.

        Returns
        -------
        str
            Valid access token for API calls.

        Raises
        ------
        AuthenticationError
            If no valid token is available and refresh fails.
        """
        pass

    @property
    @abstractmethod
    def is_authenticated(self) -> bool:
        """
        Check if currently authenticated with a valid token.

        Returns
        -------
        bool
            True if a valid (non-expired) token is available.
        """
        pass

    @abstractmethod
    def revoke(self) -> None:
        """
        Revoke current authentication and clear cached tokens.

        This method should clear any cached tokens and, if supported
        by the provider, revoke the tokens on the server side.
        """
        pass
