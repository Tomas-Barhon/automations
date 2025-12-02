from email_connector import EmailConnectorFactory, settings


def main() -> None:
    """Fetch and display recent emails from Outlook."""
    config = settings.get_outlook_config()
    connector = EmailConnectorFactory.create("outlook", config.to_dict())

    with connector:
        messages = connector.get_messages("inbox", limit=5)
        print(f"Retrieved {len(messages)} messages:\n")
        for msg in messages:
            print(f"From: {msg.sender_name} <{msg.sender}>")
            print(f"Subject: {msg.subject}")
            print(f"Date: {msg.received_at}")
            print("-" * 50)


if __name__ == "__main__":
    main()
