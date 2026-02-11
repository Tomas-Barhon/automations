"""Factory for creating email connectors.

This module provides a factory pattern for instantiating
email connectors based on provider type.
"""

import logging
from pathlib import Path
from typing import Any, Literal

from email_connector.interfaces.connector import EmailConnector
from email_connector.providers.outlook.auth import MSGraphAuthProvider
from email_connector.providers.outlook.connector import OutlookConnector

logger = logging.getLogger(__name__)

ProviderType = Literal["outlook", "gmail", "imap"]


class EmailConnectorFactory:
    """
    Factory for creating email connectors.

    This factory encapsulates the logic for creating provider-specific
    connector instances, hiding implementation details from client code.

    Examples
    --------
    >>> config = {
    ...     "client_id": "your-client-id",
    ...     "tenant_id": "your-tenant-id",
    ... }
    >>> connector = EmailConnectorFactory.create("outlook", config)
    >>> with connector:
    ...     folders = connector.list_folders()
    """

    @staticmethod
    def create(
        provider: ProviderType,
        config: dict[str, Any],
    ) -> EmailConnector:
        """
        Create an email connector for the specified provider.

        Parameters
        ----------
        provider : ProviderType
            Email provider type ("outlook", "gmail", "imap").
        config : dict[str, Any]
            Provider-specific configuration.

        Returns
        -------
        EmailConnector
            Configured connector instance.

        Raises
        ------
        NotImplementedError
            If provider is not supported.
        ValueError
            If required configuration is missing.

        Notes
        -----
        Outlook configuration:
            - client_id: str (required)
            - tenant_id: str (required)
            - client_secret: str (optional, for app-only access)
            - user_id: str (optional, default "me")
            - token_cache_path: str (optional)
        """
        logger.info(f"Creating email connector for provider: {provider}")

        match provider:
            case "outlook":
                return EmailConnectorFactory._create_outlook_connector(config)
            case "gmail":
                raise NotImplementedError(
                    "Gmail connector not yet implemented. "
                    "Contributions welcome!"
                )
            case "imap":
                raise NotImplementedError(
                    "IMAP connector not yet implemented. "
                    "Contributions welcome!"
                )
            case _:
                raise NotImplementedError(
                    f"Provider '{provider}' is not supported. "
                    f"Available providers: outlook"
                )

    @staticmethod
    def _create_outlook_connector(config: dict[str, Any]) -> OutlookConnector:
        """
        Create Outlook connector with MS Graph authentication.

        Parameters
        ----------
        config : dict[str, Any]
            Outlook-specific configuration.

        Returns
        -------
        OutlookConnector
            Configured Outlook connector.

        Raises
        ------
        ValueError
            If required configuration is missing.
        """
        # Validate required config
        required = ["client_id"]
        missing = [k for k in required if k not in config]
        if missing:
            raise ValueError(
                f"""Missing required configuration for Outlook:
                {", ".join(missing)}"""
            )

        # Parse token cache path if provided
        token_cache_path = None
        if "token_cache_path" in config:
            token_cache_path = Path(config["token_cache_path"])

        # Create auth provider
        auth_provider = MSGraphAuthProvider(
            client_id=config["client_id"],
            client_secret=config.get("client_secret"),
            tenant_id=config.get("tenant_id"),
            scopes=config.get("scopes"),
            token_cache_path=token_cache_path,
        )

        # Create connector
        connector = OutlookConnector(
            auth_provider=auth_provider,
            user_id=config.get("user_id", "me"),
            timeout=config.get("timeout", 30.0),
        )

        logger.debug("Outlook connector created successfully")
        return connector

    @staticmethod
    def get_supported_providers() -> list[str]:
        """
        Get list of supported provider types.

        Returns
        -------
        list[str]
            List of supported provider identifiers.
        """
        return ["outlook"]
