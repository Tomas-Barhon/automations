"""Debug script for device flow authentication with token caching."""

import os
from pathlib import Path

import msal
from dotenv import load_dotenv

load_dotenv()

# Same cache path as main.py
cache_path = Path(__file__).parent / ".cache" / "token_cache.json"
cache_path.parent.mkdir(exist_ok=True)

# Initialize token cache
token_cache = msal.SerializableTokenCache()
if cache_path.exists():
    token_cache.deserialize(cache_path.read_text())
    print(f"Loaded existing token cache from {cache_path}")

client_id = os.getenv("APPLICATION_ID")
print(f"Client ID: {client_id}")

app = msal.PublicClientApplication(
    client_id=client_id,
    authority="https://login.microsoftonline.com/consumers",
    token_cache=token_cache,
)

scopes = [
    "https://graph.microsoft.com/Mail.ReadWrite",
    "https://graph.microsoft.com/Mail.Send",
    "https://graph.microsoft.com/User.Read",
]

# Try silent auth first
accounts = app.get_accounts()
if accounts:
    print(f"Found {len(accounts)} cached account(s)")
    result = app.acquire_token_silent(scopes=scopes, account=accounts[0])
    if result and "access_token" in result:
        print("✅ Token acquired silently from cache!")
        print(f"Account: {accounts[0].get('username')}")
        exit(0)

# Need interactive auth
print("No cached token, starting device flow...")
flow = app.initiate_device_flow(scopes=scopes)

if "error" in flow:
    print(f"ERROR: {flow['error']}")
    print(f"Description: {flow.get('error_description', 'N/A')}")
    exit(1)

print(f"\n{'=' * 60}")
print(f"Go to: {flow.get('verification_uri')}")
print(f"Enter code: {flow.get('user_code')}")
print(f"{'=' * 60}\n")

# Wait for user to authenticate
result = app.acquire_token_by_device_flow(flow)

if "access_token" in result:
    print("✅ Authentication successful!")
    print(
        f"Account: {
            result.get('id_token_claims', {}).get(
                'preferred_username', 'Unknown'
            )
        }"
    )

    # Save token cache
    if token_cache.has_state_changed:
        cache_path.write_text(token_cache.serialize())
        print(f"Token cached to {cache_path}")
else:
    print(f"❌ Authentication failed: {result.get('error')}")
    print(f"Description: {result.get('error_description')}")
