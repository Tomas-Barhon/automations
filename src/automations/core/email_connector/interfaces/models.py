"""Data models for email connector.

This module contains immutable data transfer objects representing
email-related entities. All models are provider-agnostic.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto


class MessagePriority(Enum):
    """Email message priority levels."""

    LOW = auto()
    NORMAL = auto()
    HIGH = auto()


@dataclass(frozen=True)
class EmailAttachment:
    """
    Represents an email attachment.

    Attributes
    ----------
    id : str
        Unique identifier for the attachment.
    name : str
        Filename of the attachment.
    content_type : str
        MIME type of the attachment.
    size_bytes : int
        Size of the attachment in bytes.
    """

    id: str
    name: str
    content_type: str
    size_bytes: int


@dataclass(frozen=True)
class EmailFolder:
    """
    Represents an email folder or label.

    Attributes
    ----------
    id : str
        Unique identifier for the folder.
    name : str
        Display name of the folder.
    unread_count : int
        Number of unread messages in the folder.
    total_count : int
        Total number of messages in the folder.
    parent_id : str | None
        Parent folder ID if nested, None for root folders.
    """

    id: str
    name: str
    unread_count: int
    total_count: int
    parent_id: str | None = None


@dataclass(frozen=True)
class EmailMessage:
    """
    Immutable email message representation.

    This is a provider-agnostic representation of an email message.
    Implementations should map provider-specific formats to this model.

    Attributes
    ----------
    id : str
        Unique identifier for the message.
    subject : str
        Email subject line.
    sender : str
        Sender email address.
    sender_name : str
        Sender display name.
    recipients : tuple[str, ...]
        List of recipient email addresses (To field).
    cc : tuple[str, ...]
        List of CC recipient email addresses.
    body : str
        Full message body (HTML or plain text).
    body_preview : str
        Short preview of the message body.
    received_at : datetime
        When the message was received.
    is_read : bool
        Whether the message has been read.
    folder_id : str
        ID of the folder containing this message.
    priority : MessagePriority
        Message priority level.
    attachments : tuple[EmailAttachment, ...]
        List of attachments.
    labels : tuple[str, ...]
        Labels or categories applied to the message.
    conversation_id : str | None
        Thread/conversation identifier.
    """

    id: str
    subject: str
    sender: str
    sender_name: str
    recipients: tuple[str, ...]
    cc: tuple[str, ...]
    body: str
    body_preview: str
    received_at: datetime
    is_read: bool
    folder_id: str
    priority: MessagePriority = MessagePriority.NORMAL
    attachments: tuple[EmailAttachment, ...] = field(default_factory=tuple)
    labels: tuple[str, ...] = field(default_factory=tuple)
    conversation_id: str | None = None


@dataclass(frozen=True)
class MessageFilter:
    """
    Filter criteria for retrieving messages.

    Attributes
    ----------
    unread_only : bool
        Only return unread messages.
    has_attachments : bool | None
        Filter by attachment presence. None means no filter.
    from_address : str | None
        Filter by sender address.
    subject_contains : str | None
        Filter by subject substring.
    received_after : datetime | None
        Only messages received after this datetime.
    received_before : datetime | None
        Only messages received before this datetime.
    """

    unread_only: bool = False
    has_attachments: bool | None = None
    from_address: str | None = None
    subject_contains: str | None = None
    received_after: datetime | None = None
    received_before: datetime | None = None


@dataclass(frozen=True)
class ClassificationResult:
    """
    Result of email classification.

    Attributes
    ----------
    message_id : str
        ID of the classified message.
    category : str
        Assigned category/label.
    confidence : float
        Classification confidence score (0.0 to 1.0).
    suggested_folder : str | None
        Suggested folder to move the message to.
    suggested_action : str | None
        Suggested action (e.g., "archive", "reply", "delete").
    reasoning : str | None
        Explanation for the classification decision.
    """

    message_id: str
    category: str
    confidence: float
    suggested_folder: str | None = None
    suggested_action: str | None = None
    reasoning: str | None = None
