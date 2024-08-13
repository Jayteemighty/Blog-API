import secrets

# Generate a secure random key
signing_key = secrets.token_urlsafe(64)
print(signing_key)
