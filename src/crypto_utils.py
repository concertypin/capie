import os
import base64
from typing import Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# File format: MAGIC (5 bytes) + NONCE (12 bytes) + CIPHERTEXT
MAGIC = b"ENCv1"
NONCE_LEN = 12


def get_kek_from_env() -> bytes:
    """Read KEK from env `CA_KEK` (base64). Raises RuntimeError if missing/invalid."""
    b64 = os.getenv("CA_KEK")
    if not b64:
        raise RuntimeError("CA_KEK environment variable is required to decrypt keys")
    try:
        kek = base64.b64decode(b64)
    except Exception as e:
        raise RuntimeError("CA_KEK must be base64-encoded") from e
    if len(kek) not in (16, 24, 32):
        raise RuntimeError("CA_KEK must decode to 16/24/32 bytes (AES key); 32 bytes recommended")
    return kek


def encrypt_bytes(plain: bytes, kek: bytes) -> bytes:
    """Encrypt `plain` with AES-GCM using `kek`. Returns MAGiC+nonce+ciphertext."""
    aes = AESGCM(kek)
    nonce = os.urandom(NONCE_LEN)
    ct = aes.encrypt(nonce, plain, None)
    return MAGIC + nonce + ct


def decrypt_bytes(blob: bytes, kek: bytes) -> bytes:
    """Decrypt blob previously produced by `encrypt_bytes`.

    If `blob` is not in encrypted format (doesn't start with MAGIC) it is
    returned unchanged.
    """
    if not blob.startswith(MAGIC):
        return blob
    nonce = blob[len(MAGIC) : len(MAGIC) + NONCE_LEN]
    ct = blob[len(MAGIC) + NONCE_LEN :]
    aes = AESGCM(kek)
    return aes.decrypt(nonce, ct, None)


def decrypt_if_needed(blob: bytes, kek: Optional[bytes] = None) -> bytes:
    """If `blob` is encrypted (MAGIC prefix), decrypt it using provided KEK or
    `CA_KEK` from environment. Otherwise return unchanged bytes."""
    if not blob.startswith(MAGIC):
        return blob
    if kek is None:
        kek = get_kek_from_env()
    return decrypt_bytes(blob, kek)
