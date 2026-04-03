"""
Tests for Knowledge Graph Module
================================

Comprehensive test suite for TinyLedger, LedgerEntry,
and blockchain-inspired memory storage.
"""

import pytest
import time

from omninet.knowledge_graph import (
    TinyLedger,
    LedgerEntry,
    create_sovereign_ledger,
    LedgerError,
    ChainIntegrityError,
    EntryNotFoundError,
)


class TestLedgerEntry:
    """Test suite for LedgerEntry class."""

    def test_init(self):
        """Test basic initialization."""
        entry = LedgerEntry(
            timestamp=time.time(),
            key="test_key",
            value="test_value",
            prev_hash="0" * 64
        )
        assert entry.key == "test_key"
        assert entry.value == "test_value"
        assert len(entry.hash) == 64

    def test_hash_is_computed(self):
        """Test that hash is automatically computed."""
        entry = LedgerEntry(
            timestamp=12345.0,
            key="key",
            value="value",
            prev_hash="prev"
        )
        assert entry.hash != ""
        assert len(entry.hash) == 64

    def test_verify_hash_valid(self):
        """Test that valid hash verification passes."""
        entry = LedgerEntry(
            timestamp=time.time(),
            key="key",
            value="value",
            prev_hash="prev"
        )
        assert entry.verify_hash() is True

    def test_verify_hash_invalid(self):
        """Test that invalid hash verification fails."""
        entry = LedgerEntry(
            timestamp=time.time(),
            key="key",
            value="value",
            prev_hash="prev",
            hash="invalid_hash"
        )
        assert entry.verify_hash() is False

    def test_same_inputs_same_hash(self):
        """Test that same inputs produce same hash."""
        ts = time.time()
        entry1 = LedgerEntry(timestamp=ts, key="key", value="value", prev_hash="prev")
        entry2 = LedgerEntry(timestamp=ts, key="key", value="value", prev_hash="prev")
        assert entry1.hash == entry2.hash

    def test_different_inputs_different_hash(self):
        """Test that different inputs produce different hashes."""
        entry1 = LedgerEntry(timestamp=time.time(), key="key1", value="value", prev_hash="prev")
        entry2 = LedgerEntry(timestamp=time.time(), key="key2", value="value", prev_hash="prev")
        assert entry1.hash != entry2.hash

    def test_to_dict(self):
        """Test dictionary conversion."""
        entry = LedgerEntry(
            timestamp=time.time(),
            key="key",
            value="value",
            prev_hash="prev"
        )
        result = entry.to_dict()
        assert "timestamp" in result
        assert "key" in result
        assert "value" in result
        assert "prev_hash" in result
        assert "hash" in result


class TestTinyLedger:
    """Test suite for TinyLedger class."""

    def test_init_empty(self):
        """Test empty ledger initialization."""
        ledger = TinyLedger()
        assert len(ledger) == 0

    def test_add_entry(self):
        """Test adding an entry."""
        ledger = TinyLedger()
        entry = ledger.add("key1", "value1")
        assert len(ledger) == 1
        assert entry.key == "key1"
        assert entry.value == "value1"

    def test_get_entry(self):
        """Test retrieving an entry."""
        ledger = TinyLedger()
        ledger.add("key1", "value1")
        result = ledger.get("key1")
        assert result == "value1"

    def test_get_nonexistent(self):
        """Test retrieving nonexistent key."""
        ledger = TinyLedger()
        result = ledger.get("nonexistent")
        assert result is None

    def test_get_latest_value(self):
        """Test that get returns latest value for key."""
        ledger = TinyLedger()
        ledger.add("key1", "value1")
        ledger.add("key1", "value2")
        result = ledger.get("key1")
        assert result == "value2"

    def test_get_all(self):
        """Test getting all entries for a key."""
        ledger = TinyLedger()
        ledger.add("key1", "value1")
        ledger.add("key1", "value2")
        ledger.add("key2", "other")
        entries = ledger.get_all("key1")
        assert len(entries) == 2

    def test_chain_linkage(self):
        """Test that chain is properly linked."""
        ledger = TinyLedger()
        entry1 = ledger.add("key1", "value1")
        entry2 = ledger.add("key2", "value2")
        
        assert entry2.prev_hash == entry1.hash

    def test_verify_chain_empty(self):
        """Test chain verification on empty ledger."""
        ledger = TinyLedger()
        assert ledger.verify_chain() is True

    def test_verify_chain_valid(self):
        """Test chain verification on valid chain."""
        ledger = TinyLedger()
        ledger.add("key1", "value1")
        ledger.add("key2", "value2")
        ledger.add("key3", "value3")
        assert ledger.verify_chain() is True

    def test_get_latest_hash_empty(self):
        """Test getting latest hash from empty ledger."""
        ledger = TinyLedger()
        result = ledger.get_latest_hash()
        assert result == ledger.genesis_hash

    def test_get_latest_hash(self):
        """Test getting latest hash."""
        ledger = TinyLedger()
        entry = ledger.add("key1", "value1")
        result = ledger.get_latest_hash()
        assert result == entry.hash

    def test_export_chain(self):
        """Test chain export."""
        ledger = TinyLedger()
        ledger.add("key1", "value1")
        ledger.add("key2", "value2")
        exported = ledger.export_chain()
        assert len(exported) == 2
        assert all(isinstance(e, dict) for e in exported)

    def test_get_stats(self):
        """Test getting ledger stats."""
        ledger = TinyLedger()
        ledger.add("key1", "value1")
        ledger.add("key2", "value2")
        stats = ledger.get_stats()
        assert stats["entry_count"] == 2
        assert stats["unique_keys"] == 2
        assert "key1" in stats["keys"]
        assert "key2" in stats["keys"]

    def test_add_empty_key_raises(self):
        """Test that empty key raises error."""
        ledger = TinyLedger()
        with pytest.raises(LedgerError):
            ledger.add("", "value")


class TestCreateSovereignLedger:
    """Test suite for sovereign ledger factory function."""

    def test_creates_ledger(self):
        """Test that function creates a ledger."""
        ledger = create_sovereign_ledger()
        assert isinstance(ledger, TinyLedger)

    def test_has_genesis_hash(self):
        """Test that ledger has sovereign genesis hash."""
        ledger = create_sovereign_ledger()
        assert ledger.genesis_hash != "0" * 64
        assert len(ledger.genesis_hash) == 64

    def test_genesis_hash_contains_sovereign(self):
        """Test that genesis hash is derived from sovereign data."""
        ledger = create_sovereign_ledger()
        # The hash should be deterministic
        ledger2 = create_sovereign_ledger()
        assert ledger.genesis_hash == ledger2.genesis_hash
