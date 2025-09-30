from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64

public_pem = b"""-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEYNgnVwDj8jdRu6QSq3xIcydZNJeo
TToHocCTvxdkyH8jdbzOJa8zeOmrVVW+icZxK+M2ZWyRW8WHLE542iWqeA==
-----END PUBLIC KEY-----"""

# PEM → 公開鍵オブジェクト
public_key_obj = serialization.load_pem_public_key(public_pem, backend=default_backend())

# 公開鍵オブジェクト → raw bytes (X9.62 uncompressed point)
raw_bytes = public_key_obj.public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint
)

# raw bytes → Base64URL文字列
public_key_b64url = base64.urlsafe_b64encode(raw_bytes).decode().rstrip('=')
print("PUBLIC KEY for Vue:", public_key_b64url)
