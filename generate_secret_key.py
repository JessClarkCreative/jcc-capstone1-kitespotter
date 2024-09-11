import os
import base64

# Generate a random secret key
secret_key = os.urandom(24)
# Encode the key in Base64 to make it a readable string
encoded_key = base64.b64encode(secret_key).decode('utf-8')
# Print the key as a string
print(encoded_key)
