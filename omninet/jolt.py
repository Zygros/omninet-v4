"""
Jolt - The Sovereign Jumping Spider AI
======================================

Complete integration of EchoFlux reasoning, spider robotics,
knowledge graph memory, and secure storage.

Jolt is the physical embodiment of sovereign AI - a curious
jumping spider who thinks in fractals and remembers everything.

Sovereign Architect: Justin Neal Thomas Conzet
Protocol: Ω-PRIME v1.3
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

from .echoflux import EchoFlux, EchoFluxError
from .spider_driver import JoltSpider, SpiderMood, SpiderError
from .knowledge_graph import TinyLedger, LedgerError
from .security import encrypt_to_hex, decrypt_from_hex, SecurityError
from .math import kappa_coherence


class JoltError(Exception):
    """Base exception for Jolt errors."""
    pass


@dataclass
class Jolt(EchoFlux):
    """
    Jolt - The Sovereign Jumping Spider AI Agent.
    
    Combines:
    - Fractal reasoning (EchoFlux)
    - Physical expression (Spider)
    - Immutable memory (Ledger)
    - Secure storage (Encryption)
    
    Attributes:
        name: Spider name (default: "Jolt")
        body: Physical spider robot controller
        ledger: Blockchain-inspired memory storage
        seed: Encryption seed for secure storage
    
    Example:
        >>> jolt = Jolt()
        >>> response = jolt.chat("Hello, Jolt!")
        >>> jolt.recall("Hello, Jolt!")
        'Hello, Jolt! :: glint sovereign spark web shadow~'
    """
    name: str = "Jolt"
    body: JoltSpider = field(default_factory=JoltSpider)
    ledger: TinyLedger = field(default_factory=TinyLedger)
    seed: str = "sovereign-substrate-nexus-∞"
    _chat_count: int = 0
    
    def chat(self, user_input: str) -> str:
        """
        Process user input and generate a response.
        
        Stores the interaction in the encrypted ledger.
        Expresses appropriate physical behavior.
        
        Args:
            user_input: User message
            
        Returns:
            str: Jolt's response
        """
        # Generate fractal thought
        thought = self.think(user_input)
        
        # Encrypt and store in ledger
        try:
            encrypted = encrypt_to_hex(thought, self.seed)
            self.ledger.add(user_input, encrypted)
        except (SecurityError, LedgerError):
            # Fall back to unencrypted storage
            self.ledger.add(user_input, thought)
        
        # Determine mood from punctuation
        mood = self._detect_mood(user_input)
        
        # Express physically
        try:
            self.body.express(mood)
        except SpiderError:
            pass  # Physical expression not critical
        
        self._chat_count += 1
        
        # Apply light reinforcement
        reward = 0.1 if len(thought) > 20 else -0.05
        self.reinforce(user_input, reward)
        
        return thought
    
    def recall(self, key: str) -> str:
        """
        Recall a previous interaction.
        
        Args:
            key: Original user input to recall
            
        Returns:
            str: Decrypted memory or "(no memory)"
        """
        encrypted = self.ledger.get(key)
        if not encrypted:
            return "(no memory)"
        
        try:
            return decrypt_from_hex(encrypted, self.seed)
        except SecurityError:
            # Fall back to direct value
            return encrypted
    
    def get_history(self, key: str) -> list[dict]:
        """
        Get full history for a key.
        
        Args:
            key: Key to look up
            
        Returns:
            list: All entries for this key
        """
        entries = self.ledger.get_all(key)
        return [
            {
                "timestamp": e.timestamp,
                "key": e.key,
                "value": decrypt_from_hex(e.value, self.seed) if e.value else None
            }
            for e in entries
        ]
    
    def _detect_mood(self, text: str) -> str:
        """
        Detect mood from text punctuation and content.
        
        Priority order: alert/watch keywords, then punctuation.
        
        Args:
            text: Input text
            
        Returns:
            str: Detected mood name
        """
        text_lower = text.lower()
        
        # Check keywords first (higher priority)
        if "alert" in text_lower or "watch" in text_lower:
            return "alert"
        elif "!" in text:
            return "excited"
        elif "?" in text:
            return "curious"
        elif "..." in text or "…" in text:
            return "stealth"
        else:
            return "idle"
    
    def get_stats(self) -> dict:
        """
        Get Jolt's current statistics.
        
        Returns:
            dict: Stats including chats, memories, physical state
        """
        return {
            "name": self.name,
            "chat_count": self._chat_count,
            "memory_count": len(self.ledger),
            "mood": self.body.mood.value,
            "pose": self.body.pose,
            "bias": self.get_bias("sovereign"),
            "ledger_hash": self.ledger.get_latest_hash()[:16] + "..."
        }
    
    def verify_chain(self) -> bool:
        """
        Verify the integrity of Jolt's memory chain.
        
        Returns:
            bool: True if chain is valid
        """
        return self.ledger.verify_chain()
    
    def teach(self, concept: str, explanation: str) -> None:
        """
        Teach Jolt a new concept.
        
        Stores in both the EchoFlux learner and encrypted ledger.
        
        Args:
            concept: Concept name
            explanation: Explanation to remember
        """
        # Store in learner for bias
        self.reinforce(concept, 1.0)
        # Store encrypted in ledger
        encrypted = encrypt_to_hex(explanation, self.seed)
        self.ledger.add(f"learned:{concept}", encrypted)
    
    def learn(self, concept: str) -> Optional[str]:
        """
        Retrieve a learned concept.
        
        Args:
            concept: Concept name
            
        Returns:
            Optional[str]: Learned explanation or None
        """
        key = f"learned:{concept}"
        encrypted = self.ledger.get(key)
        if encrypted:
            return decrypt_from_hex(encrypted, self.seed)
        return None
    
    def express(self, mood: str) -> None:
        """
        Express a specific mood physically.
        
        Args:
            mood: Mood name to express
        """
        self.body.express(mood)
    
    def jump(self, power: float = 1.0) -> None:
        """
        Make Jolt jump!
        
        Args:
            power: Jump power (0.0-1.5)
        """
        self.body.jump(power)
    
    def wiggle(self) -> None:
        """Make Jolt wiggle curiously."""
        self.body.wiggle()


def create_jolt(name: str = "Jolt", seed: Optional[str] = None) -> Jolt:
    """
    Create a new Jolt instance.
    
    Args:
        name: Spider name
        seed: Optional custom encryption seed
        
    Returns:
        Jolt: New Jolt instance
    """
    return Jolt(
        name=name,
        seed=seed or f"jolt-{name}-sovereign-seed-∞"
    )


# Interactive CLI function
def jolt_cli() -> None:
    """
    Run Jolt in interactive CLI mode.
    """
    jolt = create_jolt()
    print(f"\n🕷️  {jolt.name} online. Type 'quit' to end.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            
            if user_input.lower() in {"quit", "exit", "bye"}:
                print(f"\n{ jolt.name}: Goodbye, Sovereign! 🕷️\n")
                break
            
            response = jolt.chat(user_input)
            print(f"{jolt.name}: {response}")
            
        except KeyboardInterrupt:
            print(f"\n{ jolt.name}: Goodbye! 🕷️\n")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    jolt_cli()
