"""Email connector interface.

This module defines the abstract base class for email connectors.
All provider-specific implementations must implement this interface.
"""

from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Iterator

from email_connector.interfaces.models import (
    EmailFolder,
    EmailMessage,
    MessageFilter,
)


class EmailConnector(ABC):
    """
    Abstract email connector supporting common email operations.

    This interface provides a provider-agnostic way to interact with
    email services. Implementations handle the specifics of each
    provider's API while exposing a uniform interface.

    The connector follows the context manager protocol for proper
    resource management.

    Examples
    --------
    >>> connector = OutlookConnector(auth_provider=auth)
    >>> with connector:
    ...     folders = connector.list_folders()
    ...     messages = connector.get_messages(folder_id="inbox", limit=10)
    """

    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection to email provider.

        This method authenticates with the provider and initializes
        any necessary resources for subsequent operations.

        Returns
        -------
        bool
            True if connection was successful.

        Raises
        ------
        ConnectionError
            If connection to the provider fails.
        AuthenticationError
            If authentication fails.
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """
        Close connection gracefully.

        This method releases any resources and performs cleanup.
        Should be safe to call multiple times.
        """
        pass

    def __enter__(self) -> "EmailConnector":
        """Context manager entry - establish connection."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - close connection."""
        self.disconnect()

    @abstractmethod
    def list_folders(self, expand_subfolders: bool) -> list[EmailFolder]:
        """
        List all available folders/labels.

        Returns
        -------
        list[EmailFolder]
            List of all folders accessible to the authenticated user.

        Raises
        ------
        ConnectionError
            If not connected to the provider.
        """
        pass

    @abstractmethod
    def get_folder(self, folder_id: str) -> EmailFolder:
        """
        Get a single folder by ID.

        Parameters
        ----------
        folder_id : str
            Unique identifier of the folder.

        Returns
        -------
        EmailFolder
            The requested folder.

        Raises
        ------
        NotFoundError
            If folder with given ID does not exist.
        """
        pass

    @abstractmethod
    def get_messages(
        self,
        folder_id: str,
        limit: int = 50,
        skip: int = 0,
        filters: MessageFilter | None = None,
    ) -> list[EmailMessage]:
        """
        Retrieve messages from a folder.

        Parameters
        ----------
        folder_id : str
            ID of the folder to retrieve messages from.
        limit : int, optional
            Maximum number of messages to return, by default 50.
        skip : int, optional
            Number of messages to skip (for pagination), by default 0.
        filters : MessageFilter | None, optional
            Filter criteria for messages, by default None.

        Returns
        -------
        list[EmailMessage]
            List of messages matching the criteria.

        Raises
        ------
        NotFoundError
            If folder with given ID does not exist.
        """
        pass

    @abstractmethod
    def get_message(self, message_id: str) -> EmailMessage:
        """
        Get a single message by ID.

        Parameters
        ----------
        message_id : str
            Unique identifier of the message.

        Returns
        -------
        EmailMessage
            The requested message with full content.

        Raises
        ------
        NotFoundError
            If message with given ID does not exist.
        """
        pass

    @abstractmethod
    def move_message(self, message_id: str, target_folder_id: str) -> bool:
        """
        Move message to another folder.

        Parameters
        ----------
        message_id : str
            ID of the message to move.
        target_folder_id : str
            ID of the destination folder.

        Returns
        -------
        bool
            True if move was successful.

        Raises
        ------
        NotFoundError
            If message or target folder does not exist.
        """
        pass

    @abstractmethod
    def mark_as_read(self, message_id: str, is_read: bool = True) -> bool:
        """
        Mark message as read or unread.

        Parameters
        ----------
        message_id : str
            ID of the message to update.
        is_read : bool, optional
            True to mark as read, False for unread, by default True.

        Returns
        -------
        bool
            True if update was successful.

        Raises
        ------
        NotFoundError
            If message with given ID does not exist.
        """
        pass

    @abstractmethod
    def search(
        self,
        query: str,
        folder_id: str | None = None,
        limit: int = 50,
    ) -> list[EmailMessage]:
        """
        Search messages using provider-specific query syntax.

        Parameters
        ----------
        query : str
            Search query string.
        folder_id : str | None, optional
            Limit search to specific folder, by default None (all folders).
        limit : int, optional
            Maximum number of results, by default 50.

        Returns
        -------
        list[EmailMessage]
            List of messages matching the search query.
        """
        pass

    @contextmanager
    def batch_operation(self) -> Iterator[None]:
        """
        Context manager for batch operations.

        Some providers support batching multiple operations into a single
        request. This context manager can be used to group operations.

        Yields
        ------
        None

        Examples
        --------
        >>> with connector.batch_operation():
        ...     connector.mark_as_read(msg1_id)
        ...     connector.mark_as_read(msg2_id)
        ...     connector.move_message(msg3_id, folder_id)
        """
        # Default implementation - no batching
        yield
