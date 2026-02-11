"""Outlook/Microsoft 365 email provider implementation."""

from email_connector.providers.outlook.auth import MSGraphAuthProvider
from email_connector.providers.outlook.connector import OutlookConnector

__all__ = [
    "MSGraphAuthProvider",
    "OutlookConnector",
]
