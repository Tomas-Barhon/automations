"""Email connector interfaces and data models."""

from email_connector.interfaces.auth import EmailAuthProvider
from email_connector.interfaces.classifier import EmailClassifier
from email_connector.interfaces.connector import EmailConnector
from email_connector.interfaces.models import (
    ClassificationResult,
    EmailAttachment,
    EmailFolder,
    EmailMessage,
    MessageFilter,
)

__all__ = [
    "ClassificationResult",
    "EmailAttachment",
    "EmailAuthProvider",
    "EmailClassifier",
    "EmailConnector",
    "EmailFolder",
    "EmailMessage",
    "MessageFilter",
]
