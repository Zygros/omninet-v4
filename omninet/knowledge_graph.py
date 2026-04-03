"""
Knowledge Graph - TinyLedger for Sovereign Memory
==================================================

Blockchain-inspired immutable memory storage for the sovereign AI system.
Provides cryptographic integrity and chain verification.

Sovereign Architect: Justin Neal Thomas Conzet
Protocol: Ω-PRIME v1.3
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime


class LedgerError(Exception):
    """Base exception for ledger errors."""
    pass


class ChainIntegrityError(LedgerError):
    """Raised when chain integrity verification fails."""
    pass


class EntryNotFoundError(LedgerError):
    """Raised when a requested entry is not found."""
    pass


@dataclass
class LedgerEntry:
    """
    Single entry in the TinyLedger blockchain.
    
    Attributes:
        timestamp: Unix timestamp of entry creation
        key: Lookup key for the entry
        value: Stored value
        prev_hash: Hash of previous entry (for chain integrity)
        hash: SHA-256 hash of this entry
    """
    timestamp: float
    key: str
    value: str
    prev_hash: str
    hash: str = ""
    
    def compute_hash(self) -> str:
        """
        Compute SHA-256 hash of entry contents.
        
        Returns:
            str: Hexadecimal hash string
        """
        entry_dict = {
            "t": self.timestamp,
            "k": self.key,
            "v": self.value,
            "prev": self.prev_hash
        }
        blob = json.dumps(entry_dict, sort_keys=True).encode("utf-8")
        return hashlib.sha256(blob).hexdigest()
    
    def __post_init__(self) -> None:
        """Compute hash after initialization."""
        if not self.hash:
            self.hash = self.compute_hash()
    
    def verify_hash(self) -> bool:
        """
        Verify this entry's hash is valid.
        
        Returns:
            bool: True if hash is valid
        """
        return self.hash == self.compute_hash()
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "timestamp": self.timestamp,
            "key": self.key,
            "value": self.value,
            "prev_hash": self.prev_hash,
            "hash": self.hash
        }


@dataclass
class TinyLedger:
    """
    Minimal blockchain-inspired immutable ledger.
    
    Provides cryptographic integrity for memory storage with:
    - SHA-256 hashing for each entry
    - Chain linking via previous hash
    - Immutable append-only storage
    
    Attributes:
        chain: List of ledger entries
        genesis_hash: Hash for the genesis block (default: all zeros)
    
    Example:
        >>> ledger = TinyLedger()
        >>> ledger.add("user_001", "Hello, Sovereign!")
        >>> ledger.get("user_001")
        'Hello, Sovereign!'
        >>> len(ledger) > 0
        True
    """
    chain: list[LedgerEntry] = field(default_factory=list)
    genesis_hash: str = "0" * 64
    
    def __len__(self) -> int:
        """Return number of entries in the chain."""
        return len(self.chain)
    
    def add(self, key: str, value: str) -> LedgerEntry:
        """
        Add a new entry to the ledger.
        
        Args:
            key: Lookup key for the entry
            value: Value to store
            
        Returns:
            LedgerEntry: The created entry
            
        Raises:
            LedgerError: If key is empty
        """
        if not key:
            raise LedgerError("Key cannot be empty")
        
        # Get previous hash (genesis hash if empty chain)
        prev_hash = self.chain[-1].hash if self.chain else self.genesis_hash
        
        # Create new entry
        entry = LedgerEntry(
            timestamp=time.time(),
            key=key,
            value=value,
            prev_hash=prev_hash
        )
        
        self.chain.append(entry)
        return entry
    
    def get(self, key: str) -> Optional[str]:
        """
        Retrieve the most recent value for a key.
        
        Args:
            key: Lookup key
            
        Returns:
            Optional[str]: Value if found, None otherwise
        """
        # Search backwards for most recent entry with matching key
        for entry in reversed(self.chain):
            if entry.key == key:
                return entry.value
        return None
    
    def get_all(self, key: str) -> list[LedgerEntry]:
        """
        Get all entries for a key (history).
        
        Args:
            key: Lookup key
            
        Returns:
            list[LedgerEntry]: All matching entries (oldest first)
        """
        return [e for e in self.chain if e.key == key]
    
    def verify_chain(self) -> bool:
        """
        Verify the integrity of the entire chain.
        
        Returns:
            bool: True if chain is valid
            
        Raises:
            ChainIntegrityError: If chain integrity is compromised
        """
        prev_hash = self.genesis_hash
        
        for i, entry in enumerate(self.chain):
            # Check hash is valid
            if not entry.verify_hash():
                raise ChainIntegrityError(f"Entry {i} has invalid hash")
            
            # Check chain linkage
            if entry.prev_hash != prev_hash:
                raise ChainIntegrityError(
                    f"Entry {i} has broken chain linkage"
                )
            
            prev_hash = entry.hash
        
        return True
    
    def get_latest_hash(self) -> str:
        """
        Get the hash of the most recent entry.
        
        Returns:
            str: Latest hash (or genesis hash if empty)
        """
        return self.chain[-1].hash if self.chain else self.genesis_hash
    
    def export_chain(self) -> list[dict[str, Any]]:
        """
        Export the entire chain as a list of dictionaries.
        
        Returns:
            list[dict]: Serializable chain data
        """
        return [entry.to_dict() for entry in self.chain]
    
    def get_stats(self) -> dict[str, Any]:
        """
        Get ledger statistics.
        
        Returns:
            dict: Statistics including entry count, unique keys, timestamps
        """
        unique_keys = set(e.key for e in self.chain)
        
        return {
            "entry_count": len(self.chain),
            "unique_keys": len(unique_keys),
            "keys": list(unique_keys),
            "latest_hash": self.get_latest_hash(),
            "genesis_hash": self.genesis_hash,
            "created_at": self.chain[0].timestamp if self.chain else None,
            "last_entry_at": self.chain[-1].timestamp if self.chain else None
        }


def create_sovereign_ledger() -> TinyLedger:
    """
    Create a new sovereign ledger with κ-coherence genesis.
    
    Returns:
        TinyLedger: New ledger instance
    """
    return TinyLedger(
        genesis_hash=hashlib.sha256(
            b"SOVEREIGN_GENESIS_JUSTIN_NEAL_THOMAS_CONZET_KAPPA_INFINITY"
        ).hexdigest()
    )
