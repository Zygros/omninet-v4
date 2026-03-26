"""
Security - Sovereign Encryption Module
======================================

Cryptographic utilities for secure memory storage and communication.
Implements XOR stream cipher with SHA-512 key derivation.

Sovereign Architect: Justin Neal Thomas Conzet
Protocol: Ω-PRIME v1.3
"""

from __future__ import annotations

import hashlib
import secrets
import base64
from typing import Union
from dataclasses import dataclass


class SecurityError(Exception):
    """Base exception for security errors."""
    pass


class EncryptionError(SecurityError):
    """Raised when encryption fails."""
    pass


class DecryptionError(SecurityError):
    """Raised when decryption fails."""
    pass


class InvalidKeyError(SecurityError):
    """Raised when key is invalid."""
    pass


def derive_key(seed: str, salt: str = "") -> bytes:
    """
    Derive a 64-byte encryption key from a seed string.
    
    Uses SHA-512 for key derivation with optional salt.
    
    Args:
        seed: Seed string for key derivation
        salt: Optional salt for additional security
        
    Returns:
        bytes: 64-byte derived key
        
    Raises:
        InvalidKeyError: If seed is empty
    """
    if not seed:
        raise InvalidKeyError("Seed cannot be empty")
    
    combined = f"{seed}:{salt}" if salt else seed
    return hashlib.sha512(combined.encode("utf-8")).digest()


def xor_stream(data: bytes, key: bytes) -> bytes:
    """
    Apply XOR stream cipher to data.
    
    This is a symmetric operation: xor_stream(xor_stream(data, key), key) == data
    
    Args:
        data: Data to encrypt/decrypt
        key: Key for XOR operation (will cycle if shorter than data)
        
    Returns:
        bytes: XOR'd result
    """
    key_len = len(key)
    return bytes([b ^ key[i % key_len] for i, b in enumerate(data)])


def encrypt(msg: str, seed: str, salt: str = "") -> bytes:
    """
    Encrypt a string message using XOR stream cipher.
    
    Args:
        msg: Message to encrypt
        seed: Seed for key derivation
        salt: Optional salt for additional security
        
    Returns:
        bytes: Encrypted message
        
    Raises:
        EncryptionError: If encryption fails
    """
    try:
        if not msg:
            return b""
        
        key = derive_key(seed, salt)
        return xor_stream(msg.encode("utf-8"), key)
    except Exception as e:
        raise EncryptionError(f"Encryption failed: {e}") from e


def decrypt(blob: bytes, seed: str, salt: str = "") -> str:
    """
    Decrypt a message encrypted with encrypt().
    
    Args:
        blob: Encrypted bytes
        seed: Seed used for key derivation (must match encryption)
        salt: Salt used for key derivation (must match encryption)
        
    Returns:
        str: Decrypted message
        
    Raises:
        DecryptionError: If decryption fails
    """
    try:
        if not blob:
            return ""
        
        key = derive_key(seed, salt)
        return xor_stream(blob, key).decode("utf-8", errors="ignore")
    except Exception as e:
        raise DecryptionError(f"Decryption failed: {e}") from e


def encrypt_to_hex(msg: str, seed: str, salt: str = "") -> str:
    """
    Encrypt message and return as hex string.
    
    Args:
        msg: Message to encrypt
        seed: Seed for key derivation
        salt: Optional salt
        
    Returns:
        str: Hex-encoded encrypted message
    """
    encrypted = encrypt(msg, seed, salt)
    return encrypted.hex()


def decrypt_from_hex(hex_str: str, seed: str, salt: str = "") -> str:
    """
    Decrypt a hex-encoded encrypted message.
    
    Args:
        hex_str: Hex-encoded encrypted message
        seed: Seed for key derivation
        salt: Optional salt
        
    Returns:
        str: Decrypted message
    """
    blob = bytes.fromhex(hex_str)
    return decrypt(blob, seed, salt)


def encrypt_to_base64(msg: str, seed: str, salt: str = "") -> str:
    """
    Encrypt message and return as base64 string.
    
    Args:
        msg: Message to encrypt
        seed: Seed for key derivation
        salt: Optional salt
        
    Returns:
        str: Base64-encoded encrypted message
    """
    encrypted = encrypt(msg, seed, salt)
    return base64.b64encode(encrypted).decode("utf-8")


def decrypt_from_base64(b64_str: str, seed: str, salt: str = "") -> str:
    """
    Decrypt a base64-encoded encrypted message.
    
    Args:
        b64_str: Base64-encoded encrypted message
        seed: Seed for key derivation
        salt: Optional salt
        
    Returns:
        str: Decrypted message
    """
    blob = base64.b64decode(b64_str.encode("utf-8"))
    return decrypt(blob, seed, salt)


@dataclass
class SovereignVault:
    """
    Secure vault for storing encrypted sovereign memories.
    
    Provides a high-level interface for encrypting and storing
    sensitive data with a master key.
    
    Attributes:
        master_seed: Master seed for all encryption
        salt: Optional salt for additional security
    
    Example:
        >>> vault = SovereignVault("my-secret-seed")
        >>> vault.store("password", "super_secret_123")
        >>> vault.retrieve("password")
        'super_secret_123'
    """
    master_seed: str
    salt: str = ""
    _storage: dict[str, str] = None  # type: ignore
    
    def __post_init__(self) -> None:
        """Initialize storage dictionary."""
        if self._storage is None:
            self._storage = {}
    
    def store(self, key: str, value: str) -> None:
        """
        Store an encrypted value.
        
        Args:
            key: Storage key
            value: Value to encrypt and store
        """
        encrypted = encrypt_to_hex(value, self.master_seed, self.salt)
        self._storage[key] = encrypted
    
    def retrieve(self, key: str) -> str:
        """
        Retrieve and decrypt a value.
        
        Args:
            key: Storage key
            
        Returns:
            str: Decrypted value
            
        Raises:
            KeyError: If key not found
        """
        if key not in self._storage:
            raise KeyError(f"Key not found: {key}")
        
        return decrypt_from_hex(self._storage[key], self.master_seed, self.salt)
    
    def delete(self, key: str) -> bool:
        """
        Delete a stored value.
        
        Args:
            key: Storage key
            
        Returns:
            bool: True if deleted, False if not found
        """
        if key in self._storage:
            del self._storage[key]
            return True
        return False
    
    def list_keys(self) -> list[str]:
        """
        List all stored keys.
        
        Returns:
            list[str]: List of storage keys
        """
        return list(self._storage.keys())
    
    def clear(self) -> None:
        """Clear all stored values."""
        self._storage.clear()


def generate_secure_token(length: int = 32) -> str:
    """
    Generate a cryptographically secure random token.
    
    Args:
        length: Token length in bytes (output is 2x this in hex)
        
    Returns:
        str: Hex-encoded secure token
    """
    return secrets.token_hex(length)
