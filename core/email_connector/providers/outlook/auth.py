"""Microsoft Graph API authentication provider.

This module implements OAuth2 authentication for Microsoft Graph API
using MSAL (Microsoft Authentication Library).
"""

import logging
from pathlib import Path
from typing import Any

import msal
from email_connector.exceptions import AuthenticationError
from email_connector.interfaces.auth import EmailAuthProvider

logger = logging.getLogger(__name__)


class MSGraphAuthProvider(EmailAuthProvider):
    """
    Microsoft Graph API authentication provider using MSAL.

    Supports both interactive (delegated) and client credentials
    (application) authentication flows.

    Parameters
    ----------
    client_id : str
        Azure AD application (client) ID.
    client_secret : str | None, optional
        Client secret for confidential client flow, by default None.
    scopes : list[str] | None, optional
        OAuth scopes to request. Defaults to Mail.ReadWrite.
    token_cache_path : Path | None, optional
        Path to persist token cache, by default None (no persistence).

    Examples
    --------
    >>> auth = MSGraphAuthProvider(
    ...     client_id="your-client-id",
    ... )
    >>> if auth.authenticate():
    ...     token = auth.get_access_token()
    """

    DEFAULT_SCOPES = [
        "https://graph.microsoft.com/Mail.ReadWrite",
        "https://graph.microsoft.com/Mail.Send",
        "https://graph.microsoft.com/User.Read",
    ]

    def __init__(
        self,
        client_id: str,
        client_secret: str | None = None,
        tenant_id: str | None = None,
        scopes: list[str] | None = None,
        token_cache_path: Path | None = None,
    ) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._tenant_id = tenant_id
        self._scopes = scopes or self.DEFAULT_SCOPES
        self._token_cache_path = token_cache_path

        self._token_cache = self._init_token_cache()
        self._app = self._create_msal_app()
        self._access_token: str | None = None
        self._account: dict[str, Any] | None = None

    def _init_token_cache(self) -> msal.SerializableTokenCache:
        """
        Initialize token cache with optional persistence.

        Returns
        -------
        msal.SerializableTokenCache
            Token cache instance.
        """
        cache = msal.SerializableTokenCache()

        if self._token_cache_path and self._token_cache_path.exists():
            logger.debug(f"Loading token cache from {self._token_cache_path}")
            cache.deserialize(self._token_cache_path.read_text())

        return cache

    def _save_token_cache(self) -> None:
        """Persist token cache to disk if path is configured."""
        if self._token_cache_path and self._token_cache.has_state_changed:
            logger.debug(f"Saving token cache to {self._token_cache_path}")
            self._token_cache_path.parent.mkdir(parents=True, exist_ok=True)
            self._token_cache_path.write_text(self._token_cache.serialize())

    def _create_msal_app(self) -> msal.ClientApplication:
        """
        Create MSAL application instance.

        Returns
        -------
        msal.ClientApplication
            Configured MSAL app (Public or Confidential).
        """
        # Use tenant_id if provided, otherwise 'common' for multi-tenant
        # 'common' allows both work/school and personal Microsoft accounts
        # 'consumers' is for personal accounts only
        # 'organizations' is for work/school accounts only
        tenant = self._tenant_id or "common"
        authority = f"https://login.microsoftonline.com/{tenant}"

        if self._client_secret:
            logger.debug("Creating confidential client application")
            return msal.ConfidentialClientApplication(
                client_id=self._client_id,
                client_credential=self._client_secret,
                authority=authority,
                token_cache=self._token_cache,
            )

        logger.debug("Creating public client application")
        return msal.PublicClientApplication(
            client_id=self._client_id,
            authority=authority,
            token_cache=self._token_cache,
        )

    def authenticate(self) -> bool:
        """
        Perform authentication flow.

        Attempts silent token acquisition first (from cache),
        then falls back to interactive flow for public clients
        or client credentials flow for confidential clients.

        Returns
        -------
        bool
            True if authentication was successful.

        Raises
        ------
        AuthenticationError
            If all authentication attempts fail.
        """
        # Try silent acquisition first
        result = self._acquire_token_silent()
        if result:
            logger.info("Acquired token silently from cache")
            return True

        # Fall back to appropriate flow
        if self._client_secret:
            result = self._acquire_token_client_credentials()
        else:
            result = self._acquire_token_interactive()

        if result:
            self._save_token_cache()
            return True

        raise AuthenticationError("All authentication methods failed")

    def _acquire_token_silent(self) -> bool:
        """
        Attempt silent token acquisition from cache.

        Returns
        -------
        bool
            True if token was acquired successfully.
        """
        accounts = self._app.get_accounts()
        if not accounts:
            return False

        # Use first available account
        self._account = accounts[0]
        result = self._app.acquire_token_silent(
            scopes=self._scopes,
            account=self._account,
        )

        if result and "access_token" in result:
            self._access_token = result["access_token"]
            return True

        if result and "error" in result:
            logger.warning(
                f"Silent token acquisition failed: {result['error']}"
            )

        return False

    def _acquire_token_interactive(self) -> bool:
        """
        Acquire token using device code flow.

        Displays a code for the user to enter at microsoft.com/devicelogin.
        Works in headless environments (WSL, SSH, containers).

        Returns
        -------
        bool
            True if token was acquired successfully.
        """
        logger.info("Starting device code authentication flow")

        flow = self._app.initiate_device_flow(scopes=self._scopes)

        if "user_code" not in flow:
            error = flow.get("error", "Unknown error")
            raise AuthenticationError(f"Failed to create device flow: {error}")

        # Print instructions for the user - use URL from flow response
        verification_uri = flow.get(
            "verification_uri", "https://microsoft.com/devicelogin"
        )
        print("\n" + "=" * 60)
        print("To sign in, open a browser and go to:")
        print(f"  {verification_uri}")
        print(f"\nEnter this code: {flow['user_code']}")
        print("=" * 60 + "\n")

        # Wait for user to complete authentication
        result = self._app.acquire_token_by_device_flow(flow)

        if result and "access_token" in result:
            self._access_token = result["access_token"]
            self._account = result.get("account")
            logger.info("Device code authentication successful")
            return True

        error = result.get("error", "Unknown error")
        error_description = result.get("error_description", "")
        logger.error(f"Authentication failed: {error} - {error_description}")
        raise AuthenticationError(f"{error}: {error_description}")

    def _acquire_token_client_credentials(self) -> bool:
        """
        Acquire token using client credentials flow.

        This flow is for application-only access (no user context).

        Returns
        -------
        bool
            True if token was acquired successfully.
        """
        logger.info("Acquiring token using client credentials flow")

        # Client credentials flow uses .default scope
        scopes = ["https://graph.microsoft.com/.default"]

        result = self._app.acquire_token_for_client(scopes=scopes)

        if result and "access_token" in result:
            self._access_token = result["access_token"]
            logger.info("Client credentials authentication successful")
            return True

        error = result.get("error", "Unknown error")
        error_description = result.get("error_description", "")
        logger.error(
            f"Client credentials auth failed: {error} - {error_description}"
        )
        raise AuthenticationError(f"{error}: {error_description}")

    def get_access_token(self) -> str:
        """
        Return current valid access token.

        Automatically refreshes token if expired.

        Returns
        -------
        str
            Valid access token.

        Raises
        ------
        AuthenticationError
            If no valid token is available.
        """
        if not self._access_token:
            raise AuthenticationError(
                "Not authenticated. Call authenticate() first."
            )

        # Try to refresh if we have an account (delegated auth)
        if self._account:
            result = self._app.acquire_token_silent(
                scopes=self._scopes,
                account=self._account,
            )
            if result and "access_token" in result:
                self._access_token = result["access_token"]
                self._save_token_cache()

        return self._access_token

    @property
    def is_authenticated(self) -> bool:
        """
        Check if currently authenticated.

        Returns
        -------
        bool
            True if a token is available.
        """
        return self._access_token is not None

    def revoke(self) -> None:
        """
        Clear cached tokens.

        Note: Microsoft Graph doesn't support server-side token revocation
        through MSAL, so this only clears the local cache.
        """
        logger.info("Revoking authentication - clearing token cache")
        self._access_token = None
        self._account = None

        # Clear the token cache
        if self._token_cache_path and self._token_cache_path.exists():
            self._token_cache_path.unlink()

        # Reinitialize cache and app
        self._token_cache = self._init_token_cache()
        self._app = self._create_msal_app()
