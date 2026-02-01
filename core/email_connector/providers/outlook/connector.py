"""Outlook email connector using Microsoft Graph API.

This module implements the EmailConnector interface for Microsoft 365
mailboxes using the Microsoft Graph API.
"""

import logging
from datetime import datetime
from typing import Any

import httpx
from email_connector.exceptions import (
    AuthenticationError,
    ConnectionError,
    NotFoundError,
    RateLimitError,
)
from email_connector.interfaces.auth import EmailAuthProvider
from email_connector.interfaces.connector import EmailConnector
from email_connector.interfaces.models import (
    EmailAttachment,
    EmailFolder,
    EmailMessage,
    MessageFilter,
    MessagePriority,
)

logger = logging.getLogger(__name__)


class OutlookConnector(EmailConnector):
    """
    Microsoft Outlook/365 email connector using Graph API.

    This connector provides access to Microsoft 365 mailboxes through
    the Microsoft Graph API. It requires an authenticated MSGraphAuthProvider.

    Parameters
    ----------
    auth_provider : EmailAuthProvider
        Authenticated auth provider for Graph API access.
    user_id : str, optional
        User ID or email for accessing specific mailbox.
        Default "me" uses the authenticated user's mailbox.
    timeout : float, optional
        HTTP request timeout in seconds, by default 30.0.

    Examples
    --------
    >>> auth = MSGraphAuthProvider(client_id="...", tenant_id="...")
    >>> auth.authenticate()
    >>> connector = OutlookConnector(auth_provider=auth)
    >>> with connector:
    ...     folders = connector.list_folders()
    ...     for folder in folders:
    ...         print(f"{folder.name}: {folder.unread_count} unread")
    """

    BASE_URL = "https://graph.microsoft.com/v1.0"

    def __init__(
        self,
        auth_provider: EmailAuthProvider,
        user_id: str = "me",
        timeout: float = 30.0,
    ) -> None:
        self._auth_provider = auth_provider
        self._user_id = user_id
        self._timeout = timeout
        self._client: httpx.Client | None = None
        self._connected = False

    @property
    def _base_mail_url(self) -> str:
        """Base URL for mail operations."""
        return (
            f"{self.BASE_URL}/users/{self._user_id}"
            if self._user_id != "me"
            else f"{self.BASE_URL}/me"
        )

    def _get_headers(self) -> dict[str, str]:
        """
        Get HTTP headers with current access token.

        Returns
        -------
        dict[str, str]
            Headers including Authorization.
        """
        token = self._auth_provider.get_access_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """
        Handle API response and raise appropriate exceptions.

        Parameters
        ----------
        response : httpx.Response
            HTTP response from Graph API.

        Returns
        -------
        dict[str, Any]
            Parsed JSON response.

        Raises
        ------
        NotFoundError
            If resource was not found (404).
        RateLimitError
            If rate limit was exceeded (429).
        AuthenticationError
            If authentication failed (401).
        ConnectionError
            For other HTTP errors.
        """
        if response.status_code == 200:
            return response.json()

        if response.status_code == 204:
            return {}

        if response.status_code == 401:
            raise AuthenticationError(
                "Authentication failed - token may be expired"
            )

        if response.status_code == 404:
            raise NotFoundError(f"Resource not found: {response.url}")

        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(
                "Rate limit exceeded",
                retry_after=int(retry_after) if retry_after else None,
            )

        error_data = response.json() if response.content else {}
        error_message = error_data.get("error", {}).get(
            "message", response.text
        )
        raise ConnectionError(
            f"API error ({response.status_code}): {error_message}"
        )

    def connect(self) -> bool:
        """
        Establish connection to Microsoft Graph API.

        Returns
        -------
        bool
            True if connection was successful.
        """
        if not self._auth_provider.is_authenticated:
            logger.info(
                "Auth provider not authenticated, initiating auth flow"
            )
            self._auth_provider.authenticate()

        self._client = httpx.Client(timeout=self._timeout)
        self._connected = True
        logger.info("Connected to Microsoft Graph API")
        return True

    def disconnect(self) -> None:
        """Close HTTP client and release resources."""
        if self._client:
            self._client.close()
            self._client = None
        self._connected = False
        logger.info("Disconnected from Microsoft Graph API")

    def _ensure_connected(self) -> None:
        """Raise exception if not connected."""
        if not self._connected or not self._client:
            raise ConnectionError("Not connected. Call connect() first.")

    def list_folders(self, expand_subfolders: bool) -> list[EmailFolder]:
        """
        List all mail folders.

        Parameters
        ----------
        expand_subfolders : bool
            If True, recursively retrieves all subfolders.

        Returns
        -------
        list[EmailFolder]
            List of all mail folders (flattened if expand_subfolders=True).
        """
        self._ensure_connected()
        url = f"{self._base_mail_url}/mailFolders"
        params = {"$top": 100}
        if self._client is None:
            raise ConnectionError("HTTP client is not initialized.")
        response = self._client.get(
            url, headers=self._get_headers(), params=params
        )
        data = self._handle_response(response)

        folders = []
        for item in data.get("value", []):
            folders.append(self._parse_folder(item))

            # Recursively get child folders if requested
            if expand_subfolders:
                child_folders = self._get_child_folders_recursive(item["id"])
                folders.extend(child_folders)

        logger.debug(f"Retrieved {len(folders)} mail folders")
        return folders

    def _get_child_folders_recursive(
        self, folder_id: str
    ) -> list[EmailFolder]:
        """
        Recursively retrieve all child folders for a given folder.

        Parameters
        ----------
        folder_id : str
            The ID of the parent folder.

        Returns
        -------
        list[EmailFolder]
            List of all child folders (recursively).
        """
        url = f"{self._base_mail_url}/mailFolders/{folder_id}/childFolders"
        params = {"$top": 100}

        if self._client is None:
            raise ConnectionError("HTTP client is not initialized.")
        response = self._client.get(
            url, headers=self._get_headers(), params=params
        )
        data = self._handle_response(response)

        child_folders = []
        for item in data.get("value", []):
            child_folders.append(self._parse_folder(item))

            # Recursively get grandchildren
            grandchildren = self._get_child_folders_recursive(item["id"])
            child_folders.extend(grandchildren)

        return child_folders

    def get_folder(self, folder_id: str) -> EmailFolder:
        """
        Get a single folder by ID.

        Parameters
        ----------
        folder_id : str
            Folder ID or well-known name (inbox, drafts, etc.).

        Returns
        -------
        EmailFolder
            The requested folder.
        """
        self._ensure_connected()

        url = f"{self._base_mail_url}/mailFolders/{folder_id}"
        if self._client is None:
            raise ConnectionError("HTTP client is not initialized.")
        response = self._client.get(url, headers=self._get_headers())
        data = self._handle_response(response)

        return self._parse_folder(data)

    def _parse_folder(self, data: dict[str, Any]) -> EmailFolder:
        """
        Parse Graph API folder response into EmailFolder.

        Parameters
        ----------
        data : dict[str, Any]
            Raw API response data.

        Returns
        -------
        EmailFolder
            Parsed folder object.
        """
        return EmailFolder(
            id=data["id"],
            name=data["displayName"],
            unread_count=data.get("unreadItemCount", 0),
            total_count=data.get("totalItemCount", 0),
            parent_id=data.get("parentFolderId"),
        )

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
            Folder ID or well-known name.
        limit : int, optional
            Maximum messages to return, by default 50.
        skip : int, optional
            Messages to skip for pagination, by default 0.
        filters : MessageFilter | None, optional
            Filter criteria, by default None.

        Returns
        -------
        list[EmailMessage]
            List of messages.
        """
        self._ensure_connected()

        url = f"{self._base_mail_url}/mailFolders/{folder_id}/messages"
        params = {
            "$top": limit,
            "$skip": skip,
            "$orderby": "receivedDateTime desc",
            "$select": "id,subject,from,toRecipients,ccRecipients,bodyPreview,body,"
            "receivedDateTime,isRead,parentFolderId,importance,hasAttachments,"
            "conversationId,categories",
        }

        # Build filter string
        filter_parts = self._build_filter_query(filters)
        if filter_parts:
            params["$filter"] = " and ".join(filter_parts)

        if self._client is None:
            raise ConnectionError("HTTP client is not initialized.")
        response = self._client.get(
            url, headers=self._get_headers(), params=params
        )
        data = self._handle_response(response)

        messages = [
            self._parse_message(item) for item in data.get("value", [])
        ]
        logger.debug(
            f"Retrieved {len(messages)} messages from folder {folder_id}"
        )
        return messages

    def _build_filter_query(self, filters: MessageFilter | None) -> list[str]:
        """
        Build OData filter query from MessageFilter.

        Parameters
        ----------
        filters : MessageFilter | None
            Filter criteria.

        Returns
        -------
        list[str]
            List of OData filter expressions.
        """
        if not filters:
            return []

        parts = []

        if filters.unread_only:
            parts.append("isRead eq false")

        if filters.has_attachments is not None:
            parts.append(
                f"hasAttachments eq {str(filters.has_attachments).lower()}"
            )

        if filters.from_address:
            parts.append(
                f"from/emailAddress/address eq '{filters.from_address}'"
            )

        if filters.subject_contains:
            parts.append(f"contains(subject, '{filters.subject_contains}')")

        if filters.received_after:
            iso_date = filters.received_after.isoformat()
            parts.append(f"receivedDateTime ge {iso_date}")

        if filters.received_before:
            iso_date = filters.received_before.isoformat()
            parts.append(f"receivedDateTime le {iso_date}")

        return parts

    def get_message(self, message_id: str) -> EmailMessage:
        """
        Get a single message by ID with full content.

        Parameters
        ----------
        message_id : str
            Message ID.

        Returns
        -------
        EmailMessage
            Full message with body content.
        """
        self._ensure_connected()

        url = f"{self._base_mail_url}/messages/{message_id}"
        params = {
            "$expand": "attachments($select=id,name,contentType,size)",
        }

        if self._client is None:
            raise ConnectionError("HTTP client is not initialized.")
        response = self._client.get(
            url, headers=self._get_headers(), params=params
        )
        data = self._handle_response(response)

        return self._parse_message(data)

    def _parse_message(self, data: dict[str, Any]) -> EmailMessage:
        """
        Parse Graph API message response into EmailMessage.

        Parameters
        ----------
        data : dict[str, Any]
            Raw API response data.

        Returns
        -------
        EmailMessage
            Parsed message object.
        """
        # Parse sender
        from_data = data.get("from", {}).get("emailAddress", {})
        sender = from_data.get("address", "")
        sender_name = from_data.get("name", "")

        # Parse recipients
        recipients = tuple(
            r["emailAddress"]["address"] for r in data.get("toRecipients", [])
        )
        cc = tuple(
            r["emailAddress"]["address"] for r in data.get("ccRecipients", [])
        )

        # Parse attachments
        attachments = tuple(
            EmailAttachment(
                id=a["id"],
                name=a["name"],
                content_type=a.get("contentType", "application/octet-stream"),
                size_bytes=a.get("size", 0),
            )
            for a in data.get("attachments", [])
        )

        # Parse priority
        importance = data.get("importance", "normal").lower()
        priority_map = {
            "low": MessagePriority.LOW,
            "normal": MessagePriority.NORMAL,
            "high": MessagePriority.HIGH,
        }
        priority = priority_map.get(importance, MessagePriority.NORMAL)

        # Parse body
        body_data = data.get("body", {})
        body = body_data.get("content", "")

        # Parse datetime
        received_str = data.get("receivedDateTime", "")
        received_at = datetime.fromisoformat(
            received_str.replace("Z", "+00:00")
        )

        return EmailMessage(
            id=data["id"],
            subject=data.get("subject", ""),
            sender=sender,
            sender_name=sender_name,
            recipients=recipients,
            cc=cc,
            body=body,
            body_preview=data.get("bodyPreview", ""),
            received_at=received_at,
            is_read=data.get("isRead", False),
            folder_id=data.get("parentFolderId", ""),
            priority=priority,
            attachments=attachments,
            labels=tuple(data.get("categories", [])),
            conversation_id=data.get("conversationId"),
        )

    def move_message(self, message_id: str, target_folder_id: str) -> bool:
        """
        Move message to another folder.

        Parameters
        ----------
        message_id : str
            ID of message to move.
        target_folder_id : str
            Destination folder ID.

        Returns
        -------
        bool
            True if successful.
        """
        self._ensure_connected()

        url = f"{self._base_mail_url}/messages/{message_id}/move"
        payload = {"destinationId": target_folder_id}
        if self._client is None:
            raise ConnectionError("HTTP client is not initialized.")
        response = self._client.post(
            url,
            headers=self._get_headers(),
            json=payload,
        )
        self._handle_response(response)

        logger.info(f"Moved message {message_id} to folder {target_folder_id}")
        return True

    def mark_as_read(self, message_id: str, is_read: bool = True) -> bool:
        """
        Mark message as read or unread.

        Parameters
        ----------
        message_id : str
            Message ID.
        is_read : bool, optional
            True for read, False for unread, by default True.

        Returns
        -------
        bool
            True if successful.
        """
        self._ensure_connected()

        url = f"{self._base_mail_url}/messages/{message_id}"
        payload = {"isRead": is_read}

        if self._client is None:
            raise ConnectionError("HTTP client is not initialized.")
        response = self._client.patch(
            url,
            headers=self._get_headers(),
            json=payload,
        )
        self._handle_response(response)

        status = "read" if is_read else "unread"
        logger.debug(f"Marked message {message_id} as {status}")
        return True

    def search(
        self,
        query: str,
        folder_id: str | None = None,
        limit: int = 50,
    ) -> list[EmailMessage]:
        """
        Search messages using KQL query.

        Parameters
        ----------
        query : str
            KQL search query.
        folder_id : str | None, optional
            Limit to specific folder, by default None.
        limit : int, optional
            Maximum results, by default 50.

        Returns
        -------
        list[EmailMessage]
            Matching messages.
        """
        self._ensure_connected()

        if folder_id:
            url = f"{self._base_mail_url}/mailFolders/{folder_id}/messages"
        else:
            url = f"{self._base_mail_url}/messages"

        params = {
            "$search": f'"{query}"',
            "$top": limit,
            "$select": "id,subject,from,toRecipients,ccRecipients,bodyPreview,body"
            "receivedDateTime,isRead,parentFolderId,importance,hasAttachments,"
            "conversationId,categories",
        }
        if self._client is None:
            raise ConnectionError("HTTP client is not initialized.")
        response = self._client.get(
            url, headers=self._get_headers(), params=params
        )
        data = self._handle_response(response)

        messages = [
            self._parse_message(item) for item in data.get("value", [])
        ]
        logger.debug(
            f"Search returned {len(messages)} results for query: {query}"
        )
        return messages
