from email_connector import EmailConnectorFactory, settings


def main() -> None:
    """Fetch and display recent emails from Outlook."""
    config = settings.get_outlook_config()
    connector = EmailConnectorFactory.create("outlook", config.to_dict())

    with connector:
        dirs = connector.list_folders(expand_subfolders=True)
        print("Available folders:")
        for d in dirs:
            print(f"- {d.name}")
        messages = connector.get_messages("inbox", limit=10)
        print(f"Retrieved {len(messages)} messages:\n")
        for msg in messages:
            print(f"From: {msg.sender_name} <{msg.sender}>")
            print(f"Subject: {msg.subject}")
            print(f"Date: {msg.received_at}")
            print(f"Body Preview: {msg.body_preview}")
            print("-" * 50)


if __name__ == "__main__":
    main()
