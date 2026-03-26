"""
Tests for Jolt - The Sovereign Spider AI
========================================

Comprehensive test suite for Jolt integrated agent.
"""

import pytest

from omninet.jolt import (
    Jolt,
    create_jolt,
    JoltError,
)


class TestJolt:
    """Test suite for Jolt class."""

    def test_init_defaults(self):
        """Test default initialization."""
        jolt = Jolt()
        assert jolt.name == "Jolt"
        assert jolt.body is not None
        assert jolt.ledger is not None

    def test_init_custom_name(self):
        """Test custom name initialization."""
        jolt = Jolt(name="Spark")
        assert jolt.name == "Spark"

    def test_chat_returns_string(self):
        """Test that chat returns a string."""
        jolt = Jolt()
        result = jolt.chat("Hello!")
        assert isinstance(result, str)

    def test_chat_stores_in_ledger(self):
        """Test that chat stores interaction in ledger."""
        jolt = Jolt()
        jolt.chat("test message")
        assert len(jolt.ledger) == 1

    def test_chat_increments_count(self):
        """Test that chat increments chat count."""
        jolt = Jolt()
        initial_count = jolt._chat_count
        jolt.chat("hello")
        assert jolt._chat_count == initial_count + 1

    def test_recall_returns_memory(self):
        """Test that recall returns stored memory."""
        jolt = Jolt()
        response = jolt.chat("test input")
        recalled = jolt.recall("test input")
        assert recalled == response

    def test_recall_nonexistent(self):
        """Test that recall returns placeholder for nonexistent."""
        jolt = Jolt()
        result = jolt.recall("nonexistent")
        assert result == "(no memory)"

    def test_get_history(self):
        """Test getting history."""
        jolt = Jolt()
        jolt.chat("test")
        history = jolt.get_history("test")
        assert len(history) == 1

    def test_detect_mood_excited(self):
        """Test mood detection for exclamation."""
        jolt = Jolt()
        mood = jolt._detect_mood("Hello!")
        assert mood == "excited"

    def test_detect_mood_curious(self):
        """Test mood detection for question."""
        jolt = Jolt()
        mood = jolt._detect_mood("What is this?")
        assert mood == "curious"

    def test_detect_mood_stealth(self):
        """Test mood detection for ellipsis."""
        jolt = Jolt()
        mood = jolt._detect_mood("Wait...")
        assert mood == "stealth"

    def test_detect_mood_alert(self):
        """Test mood detection for alert keyword."""
        jolt = Jolt()
        mood = jolt._detect_mood("Watch out!")
        assert mood == "alert"

    def test_detect_mood_idle(self):
        """Test mood detection for normal text."""
        jolt = Jolt()
        mood = jolt._detect_mood("Hello world")
        assert mood == "idle"

    def test_get_stats(self):
        """Test getting stats."""
        jolt = Jolt()
        jolt.chat("test")
        stats = jolt.get_stats()
        assert stats["name"] == "Jolt"
        assert stats["chat_count"] == 1
        assert stats["memory_count"] == 1

    def test_verify_chain(self):
        """Test chain verification."""
        jolt = Jolt()
        jolt.chat("test1")
        jolt.chat("test2")
        assert jolt.verify_chain() is True

    def test_teach_and_learn(self):
        """Test teaching and learning concepts."""
        jolt = Jolt()
        jolt.teach("sovereignty", "The state of being sovereign")
        result = jolt.learn("sovereignty")
        assert result == "The state of being sovereign"

    def test_learn_nonexistent(self):
        """Test learning nonexistent concept."""
        jolt = Jolt()
        result = jolt.learn("unknown")
        assert result is None

    def test_express(self):
        """Test expressing mood."""
        jolt = Jolt()
        jolt.express("curious")
        # Should not raise
        assert jolt.body.mood.value == "curious"

    def test_jump(self):
        """Test jumping."""
        jolt = Jolt()
        jolt.jump()
        # Should not raise
        assert jolt.body.pose == "jump"

    def test_wiggle(self):
        """Test wiggling."""
        jolt = Jolt()
        jolt.wiggle()
        # Should not raise
        assert jolt.body.mood.value == "curious"


class TestCreateJolt:
    """Test suite for create_jolt factory function."""

    def test_creates_jolt(self):
        """Test that function creates a Jolt instance."""
        jolt = create_jolt()
        assert isinstance(jolt, Jolt)

    def test_custom_name(self):
        """Test creating Jolt with custom name."""
        jolt = create_jolt(name="Spark")
        assert jolt.name == "Spark"

    def test_custom_seed(self):
        """Test creating Jolt with custom seed."""
        jolt = create_jolt(seed="custom_seed")
        assert jolt.seed == "custom_seed"


class TestJoltIntegration:
    """Integration tests for Jolt system."""

    def test_full_conversation_flow(self):
        """Test full conversation flow."""
        jolt = Jolt()
        
        # Chat multiple times
        r1 = jolt.chat("Hello!")
        r2 = jolt.chat("How are you?")
        r3 = jolt.chat("Tell me about sovereignty")
        
        # All should be strings
        assert isinstance(r1, str)
        assert isinstance(r2, str)
        assert isinstance(r3, str)
        
        # Stats should reflect activity
        stats = jolt.get_stats()
        assert stats["chat_count"] == 3
        assert stats["memory_count"] == 3
        
        # Chain should be valid
        assert jolt.verify_chain() is True
        
        # Should be able to recall
        assert jolt.recall("Hello!") == r1
        assert jolt.recall("How are you?") == r2

    def test_teaching_flow(self):
        """Test teaching and recalling concepts."""
        jolt = Jolt()
        
        # Teach concepts
        jolt.teach("kappa", "κ-coherence alignment metric")
        jolt.teach("phi", "Golden ratio, approximately 1.618")
        
        # Learn them back
        assert "coherence" in jolt.learn("kappa")
        assert "1.618" in jolt.learn("phi")

    def test_multiple_recall_same_key(self):
        """Test multiple recalls of same key."""
        jolt = Jolt()
        
        # Chat same input multiple times
        r1 = jolt.chat("test")
        r2 = jolt.chat("test")
        
        # Should get most recent
        assert jolt.recall("test") == r2
        
        # Should have history
        history = jolt.get_history("test")
        assert len(history) == 2
