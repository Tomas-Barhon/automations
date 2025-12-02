r"""Email connector package.

This package provides a provider-agnostic interface for email operations
with implementations for various email providers (Outlook, Gmail, etc.).

Example Usage
-------------
>>> from email_connector import EmailConnectorFactory
>>> from email_connector.classifier import RuleBasedClassifier,
sender_contains_rule
>>>
>>> # Create connector
>>> config = {"client_id": "...", "tenant_id": "..."}
>>> connector = EmailConnectorFactory.create("outlook", config)
>>>
>>> # Create classifier
>>> classifier = RuleBasedClassifier()
>>> classifier.add_rule(sender_contains_rule(
...     pattern=r"@newsletter\.",
...     category="newsletter",
...     suggested_action="archive",
... ))
>>>
>>> # Process emails
>>> with connector:
...     messages = connector.get_messages("inbox", limit=50)
...     for msg in messages:
...         result = classifier.classify(msg)
...         print(f"{msg.subject}: {result.category}")
"""

from email_connector.config import (
    EmailConnectorSettings,
    OutlookConfig,
    settings,
)
from email_connector.exceptions import (
    AuthenticationError,
    ConnectionError,
    EmailConnectorError,
    NotFoundError,
    PermissionError,
    RateLimitError,
)
from email_connector.factory import EmailConnectorFactory
from email_connector.interfaces import (
    ClassificationResult,
    EmailAttachment,
    EmailAuthProvider,
    EmailClassifier,
    EmailConnector,
    EmailFolder,
    EmailMessage,
    MessageFilter,
)

__all__ = [
    # Factory
    "EmailConnectorFactory",
    # Config
    "EmailConnectorSettings",
    "OutlookConfig",
    "settings",
    # Interfaces
    "EmailAuthProvider",
    "EmailClassifier",
    "EmailConnector",
    # Models
    "ClassificationResult",
    "EmailAttachment",
    "EmailFolder",
    "EmailMessage",
    "MessageFilter",
    # Exceptions
    "AuthenticationError",
    "ConnectionError",
    "EmailConnectorError",
    "NotFoundError",
    "PermissionError",
    "RateLimitError",
]
