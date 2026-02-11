"""Configuration management for email connector.

This module provides configuration loading and defaults for the email connector
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class OutlookConfig:
    """
    Configuration for Outlook email connector.

    Parameters
    ----------
    client_id : str
        Azure AD application (client) ID.
    tenant_id : str
        Azure AD tenant ID. Use 'consumers' for personal Microsoft accounts,
        'organizations' for work/school accounts, or a specific tenant ID.
    token_cache_path : Path | None
        Path to persist token cache for automatic token refresh.
    client_secret : str | None
        Client secret for confidential client flow (app-only access).
    scopes : list[str] | None
        OAuth scopes to request.
    user_id : str
        User ID for mailbox access. Default 'me' for authenticated user.
    timeout : float
        HTTP request timeout in seconds.
    """

    client_id: str
    tenant_id: str = "consumers"
    token_cache_path: Path | None = None
    client_secret: str | None = None
    scopes: list[str] | None = None
    user_id: str = "me"
    timeout: float = 30.0

    def to_dict(self) -> dict:
        """
        Convert config to dictionary for factory.

        Returns
        -------
        dict
            Configuration dictionary compatible with EmailConnectorFactory.
        """
        config = {
            "client_id": self.client_id,
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "timeout": self.timeout,
        }

        if self.token_cache_path:
            config["token_cache_path"] = str(self.token_cache_path)
        if self.client_secret:
            config["client_secret"] = self.client_secret
        if self.scopes:
            config["scopes"] = self.scopes

        return config


@dataclass
class EmailConnectorSettings:
    """
    Application-wide settings for email connector.

    Loads configuration from environment variables with sensible defaults.

    Parameters
    ----------
    base_dir : Path
        Base directory for storing cache and other files.
    """

    base_dir: Path = field(
        default_factory=lambda: Path(__file__).parent.parent
    )

    def __post_init__(self) -> None:
        """Load environment variables."""
        load_dotenv()

    @property
    def cache_dir(self) -> Path:
        """Get cache directory, creating if necessary."""
        cache = self.base_dir / ".cache"
        cache.mkdir(exist_ok=True)
        return cache

    @property
    def token_cache_path(self) -> Path:
        """Get token cache file path."""
        return self.cache_dir / "token_cache.json"

    def get_outlook_config(self) -> OutlookConfig:
        """
        Create OutlookConfig from environment variables.

        Returns
        -------
        OutlookConfig
            Configuration for Outlook connector.

        Raises
        ------
        ValueError
            If required environment variables are missing.
        """
        client_id = os.getenv("APPLICATION_ID")
        if not client_id:
            raise ValueError("APPLICATION_ID environment variable is required")

        return OutlookConfig(
            client_id=client_id,
            tenant_id="consumers",  # Default to personal Microsoft accounts
            token_cache_path=self.token_cache_path,
            # Don't use client_secret for personal accounts
            # (use delegated auth)
        )


# Default settings instance
settings = EmailConnectorSettings()
