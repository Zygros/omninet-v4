"""
Tests for Security Module
=========================

Comprehensive test suite for encryption, decryption,
and sovereign vault functionality.
"""

import pytest

from omninet.security import (
    encrypt,
    decrypt,
    encrypt_to_hex,
    decrypt_from_hex,
    encrypt_to_base64,
    decrypt_from_base64,
    SovereignVault,
    generate_secure_token,
    derive_key,
    xor_stream,
    SecurityError,
    EncryptionError,
    DecryptionError,
    InvalidKeyError,
)


class TestDeriveKey:
    """Test suite for key derivation."""

    def test_returns_bytes(self):
        """Test that derive_key returns bytes."""
        result = derive_key("test_seed")
        assert isinstance(result, bytes)

    def test_returns_64_bytes(self):
        """Test that derived key is 64 bytes (SHA-512)."""
        result = derive_key("test_seed")
        assert len(result) == 64

    def test_same_seed_same_key(self):
        """Test that same seed produces same key."""
        key1 = derive_key("same_seed")
        key2 = derive_key("same_seed")
        assert key1 == key2

    def test_different_seeds_different_keys(self):
        """Test that different seeds produce different keys."""
        key1 = derive_key("seed1")
        key2 = derive_key("seed2")
        assert key1 != key2

    def test_salt_affects_key(self):
        """Test that salt affects derived key."""
        key1 = derive_key("seed", salt="salt1")
        key2 = derive_key("seed", salt="salt2")
        assert key1 != key2

    def test_empty_seed_raises(self):
        """Test that empty seed raises InvalidKeyError."""
        with pytest.raises(InvalidKeyError):
            derive_key("")


class TestXorStream:
    """Test suite for XOR stream cipher."""

    def test_xor_produces_different_output(self):
        """Test that XOR produces different output."""
        data = b"hello world"
        key = b"secret"
        result = xor_stream(data, key)
        assert result != data

    def test_xor_is_symmetric(self):
        """Test that XOR is symmetric (double XOR returns original)."""
        data = b"hello world"
        key = b"secret"
        encrypted = xor_stream(data, key)
        decrypted = xor_stream(encrypted, key)
        assert decrypted == data

    def test_xor_with_longer_key(self):
        """Test XOR with key longer than data."""
        data = b"hi"
        key = b"very_long_secret_key"
        result = xor_stream(data, key)
        # Should not raise and should be reversible
        assert xor_stream(result, key) == data


class TestEncryptDecrypt:
    """Test suite for encrypt and decrypt functions."""

    def test_encrypt_returns_bytes(self):
        """Test that encrypt returns bytes."""
        result = encrypt("hello", "secret")
        assert isinstance(result, bytes)

    def test_decrypt_returns_string(self):
        """Test that decrypt returns string."""
        encrypted = encrypt("hello", "secret")
        result = decrypt(encrypted, "secret")
        assert isinstance(result, str)

    def test_roundtrip(self):
        """Test encrypt/decrypt roundtrip."""
        original = "Hello, Sovereign!"
        seed = "test_seed"
        encrypted = encrypt(original, seed)
        decrypted = decrypt(encrypted, seed)
        assert decrypted == original

    def test_different_seeds_fail(self):
        """Test that different seeds produce different results."""
        original = "secret message"
        encrypted = encrypt(original, "seed1")
        decrypted = decrypt(encrypted, "seed2")
        assert decrypted != original

    def test_empty_message(self):
        """Test encryption of empty message."""
        result = encrypt("", "seed")
        assert result == b""

    def test_unicode_message(self):
        """Test encryption of unicode message."""
        original = "你好世界 🕷️"
        encrypted = encrypt(original, "seed")
        decrypted = decrypt(encrypted, "seed")
        assert decrypted == original


class TestHexEncryption:
    """Test suite for hex encoding functions."""

    def test_encrypt_to_hex_returns_string(self):
        """Test that encrypt_to_hex returns string."""
        result = encrypt_to_hex("hello", "seed")
        assert isinstance(result, str)

    def test_decrypt_from_hex_roundtrip(self):
        """Test hex encrypt/decrypt roundtrip."""
        original = "test message"
        seed = "secret"
        encrypted = encrypt_to_hex(original, seed)
        decrypted = decrypt_from_hex(encrypted, seed)
        assert decrypted == original

    def test_hex_is_valid_hex(self):
        """Test that hex output is valid hexadecimal."""
        encrypted = encrypt_to_hex("hello", "seed")
        # Should not raise
        bytes.fromhex(encrypted)


class TestBase64Encryption:
    """Test suite for base64 encoding functions."""

    def test_encrypt_to_base64_returns_string(self):
        """Test that encrypt_to_base64 returns string."""
        result = encrypt_to_base64("hello", "seed")
        assert isinstance(result, str)

    def test_decrypt_from_base64_roundtrip(self):
        """Test base64 encrypt/decrypt roundtrip."""
        original = "test message"
        seed = "secret"
        encrypted = encrypt_to_base64(original, seed)
        decrypted = decrypt_from_base64(encrypted, seed)
        assert decrypted == original


class TestSovereignVault:
    """Test suite for SovereignVault class."""

    def test_init(self):
        """Test vault initialization."""
        vault = SovereignVault("master_seed")
        assert vault.master_seed == "master_seed"

    def test_store_and_retrieve(self):
        """Test store and retrieve operations."""
        vault = SovereignVault("master_seed")
        vault.store("key1", "value1")
        result = vault.retrieve("key1")
        assert result == "value1"

    def test_retrieve_nonexistent_raises(self):
        """Test that retrieving nonexistent key raises KeyError."""
        vault = SovereignVault("master_seed")
        with pytest.raises(KeyError):
            vault.retrieve("nonexistent")

    def test_delete(self):
        """Test delete operation."""
        vault = SovereignVault("master_seed")
        vault.store("key1", "value1")
        result = vault.delete("key1")
        assert result is True
        with pytest.raises(KeyError):
            vault.retrieve("key1")

    def test_delete_nonexistent(self):
        """Test deleting nonexistent key."""
        vault = SovereignVault("master_seed")
        result = vault.delete("nonexistent")
        assert result is False

    def test_list_keys(self):
        """Test listing keys."""
        vault = SovereignVault("master_seed")
        vault.store("key1", "value1")
        vault.store("key2", "value2")
        keys = vault.list_keys()
        assert set(keys) == {"key1", "key2"}

    def test_clear(self):
        """Test clearing vault."""
        vault = SovereignVault("master_seed")
        vault.store("key1", "value1")
        vault.clear()
        assert len(vault.list_keys()) == 0

    def test_encrypted_storage(self):
        """Test that values are encrypted in storage."""
        vault = SovereignVault("master_seed")
        vault.store("key1", "plaintext")
        # The stored value should not be plaintext
        stored = vault._storage.get("key1")
        assert stored != "plaintext"


class TestGenerateSecureToken:
    """Test suite for secure token generation."""

    def test_returns_string(self):
        """Test that generate_secure_token returns string."""
        result = generate_secure_token()
        assert isinstance(result, str)

    def test_default_length(self):
        """Test default token length (32 bytes = 64 hex chars)."""
        result = generate_secure_token()
        assert len(result) == 64

    def test_custom_length(self):
        """Test custom token length."""
        result = generate_secure_token(16)
        assert len(result) == 32  # 16 bytes = 32 hex chars

    def test_uniqueness(self):
        """Test that generated tokens are unique."""
        token1 = generate_secure_token()
        token2 = generate_secure_token()
        assert token1 != token2

    def test_is_hex(self):
        """Test that token is valid hexadecimal."""
        result = generate_secure_token()
        # Should not raise
        bytes.fromhex(result)
