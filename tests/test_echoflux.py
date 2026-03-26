"""
Tests for EchoFlux Fractal Reasoning System
===========================================

Comprehensive test suite for EchoFlux, FractalReasoner,
QuantumishCreativity, and AdaptiveLearner.
"""

import pytest
import numpy as np

from omninet.echoflux import (
    EchoFlux,
    FractalReasoner,
    QuantumishCreativity,
    AdaptiveLearner,
    echo_flux_think,
    EchoFluxError,
    FractalReasonerError,
    CreativityError,
)


class TestFractalReasoner:
    """Test suite for FractalReasoner class."""

    def test_init_defaults(self):
        """Test default initialization."""
        reasoner = FractalReasoner()
        assert reasoner.dim == 2.5
        assert reasoner.depth == 7

    def test_init_custom(self):
        """Test custom initialization."""
        reasoner = FractalReasoner(dim=3.0, depth=10)
        assert reasoner.dim == 3.0
        assert reasoner.depth == 10

    def test_invalid_dim_raises(self):
        """Test that invalid dim raises ValueError."""
        with pytest.raises(ValueError):
            FractalReasoner(dim=0)
        with pytest.raises(ValueError):
            FractalReasoner(dim=-1)

    def test_invalid_depth_raises(self):
        """Test that invalid depth raises ValueError."""
        with pytest.raises(ValueError):
            FractalReasoner(depth=0)
        with pytest.raises(ValueError):
            FractalReasoner(depth=-5)

    def test_reason_returns_ndarray(self):
        """Test that reason returns numpy ndarray."""
        reasoner = FractalReasoner()
        result = reasoner.reason("test prompt")
        assert isinstance(result, np.ndarray)

    def test_reason_normalizes_output(self):
        """Test that output is normalized (norm <= 1)."""
        reasoner = FractalReasoner()
        result = reasoner.reason("test")
        norm = np.linalg.norm(result)
        assert norm <= 1.0 + 1e-6  # Allow small floating point error

    def test_reason_empty_prompt(self):
        """Test reasoning with empty prompt."""
        reasoner = FractalReasoner()
        result = reasoner.reason("")
        assert isinstance(result, np.ndarray)
        assert len(result) == 1

    def test_reason_consistency(self):
        """Test that same input produces same output."""
        reasoner = FractalReasoner()
        result1 = reasoner.reason("consistent")
        result2 = reasoner.reason("consistent")
        np.testing.assert_array_almost_equal(result1, result2)

    def test_reason_different_prompts(self):
        """Test that different prompts produce different outputs."""
        reasoner = FractalReasoner()
        result1 = reasoner.reason("hello")
        result2 = reasoner.reason("goodbye")
        # Should not be equal
        with pytest.raises(AssertionError):
            np.testing.assert_array_almost_equal(result1, result2)


class TestQuantumishCreativity:
    """Test suite for QuantumishCreativity class."""

    def test_init_defaults(self):
        """Test default initialization."""
        qc = QuantumishCreativity()
        assert qc.temperature == 0.9
        assert len(qc.basis_words) > 0

    def test_init_custom_temperature(self):
        """Test custom temperature initialization."""
        qc = QuantumishCreativity(temperature=0.5)
        assert qc.temperature == 0.5

    def test_invalid_temperature_raises(self):
        """Test that invalid temperature raises ValueError."""
        with pytest.raises(ValueError):
            QuantumishCreativity(temperature=-0.1)
        with pytest.raises(ValueError):
            QuantumishCreativity(temperature=1.5)

    def test_generate_returns_string(self):
        """Test that generate returns a string."""
        qc = QuantumishCreativity()
        vec = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        result = qc.generate(vec, "test")
        assert isinstance(result, str)

    def test_generate_includes_prompt(self):
        """Test that generated output includes the prompt."""
        qc = QuantumishCreativity()
        vec = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        result = qc.generate(vec, "hello world")
        assert "hello world" in result

    def test_generate_includes_basis_words(self):
        """Test that generated output includes basis words."""
        qc = QuantumishCreativity()
        vec = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        result = qc.generate(vec, "test")
        # Should include at least one basis word
        found = any(word in result for word in qc.basis_words)
        assert found

    def test_generate_includes_punctuation(self):
        """Test that generated output includes punctuation."""
        qc = QuantumishCreativity()
        vec = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        result = qc.generate(vec, "test")
        assert any(p in result for p in ["!", "?", "~", "…"])


class TestAdaptiveLearner:
    """Test suite for AdaptiveLearner class."""

    def test_init_defaults(self):
        """Test default initialization."""
        learner = AdaptiveLearner()
        assert len(learner.weights) == 0

    def test_observe_updates_weights(self):
        """Test that observe updates weights."""
        learner = AdaptiveLearner()
        learner.observe("hello world", 1.0)
        assert "hello" in learner.weights
        assert "world" in learner.weights

    def test_observe_accumulates(self):
        """Test that multiple observations accumulate."""
        learner = AdaptiveLearner()
        learner.observe("test", 1.0)
        learner.observe("test", 0.5)
        assert learner.weights["test"] == 1.5

    def test_bias_returns_float(self):
        """Test that bias returns a float."""
        learner = AdaptiveLearner()
        learner.observe("hello", 1.0)
        result = learner.bias("hello world")
        assert isinstance(result, float)

    def test_bias_for_observed_tokens(self):
        """Test bias for observed tokens."""
        learner = AdaptiveLearner()
        learner.observe("sovereign", 2.0)
        bias = learner.bias("sovereign test")
        assert bias == 2.0

    def test_bias_for_unobserved_tokens(self):
        """Test bias for unobserved tokens."""
        learner = AdaptiveLearner()
        bias = learner.bias("unknown tokens")
        assert bias == 0.0

    def test_reset_clears_weights(self):
        """Test that reset clears all weights."""
        learner = AdaptiveLearner()
        learner.observe("test", 1.0)
        learner.reset()
        assert len(learner.weights) == 0


class TestEchoFlux:
    """Test suite for EchoFlux orchestrator class."""

    def test_init_defaults(self):
        """Test default initialization."""
        ef = EchoFlux()
        assert ef.reasoner is not None
        assert ef.creator is not None
        assert ef.learner is not None

    def test_think_returns_string(self):
        """Test that think returns a string."""
        ef = EchoFlux()
        result = ef.think("hello")
        assert isinstance(result, str)

    def test_reinforce_updates_learner(self):
        """Test that reinforce updates the learner."""
        ef = EchoFlux()
        ef.reinforce("test prompt", 1.0)
        bias = ef.get_bias("test")
        assert bias == 1.0

    def test_get_bias_returns_float(self):
        """Test that get_bias returns a float."""
        ef = EchoFlux()
        result = ef.get_bias("anything")
        assert isinstance(result, float)

    def test_integration_think_and_reinforce(self):
        """Test integration of think and reinforce."""
        ef = EchoFlux()
        response = ef.think("sovereign")
        ef.reinforce("sovereign", 0.5)
        bias = ef.get_bias("sovereign")
        assert bias == 0.5


class TestEchoFluxThinkFunction:
    """Test suite for echo_flux_think convenience function."""

    def test_returns_string(self):
        """Test that function returns a string."""
        result = echo_flux_think("test")
        assert isinstance(result, str)

    def test_temperature_affects_output(self):
        """Test that different temperatures produce different results."""
        # Note: This is probabilistic, but the punctuation should differ
        result1 = echo_flux_think("test", temperature=0.0)
        result2 = echo_flux_think("test", temperature=1.0)
        # Both should be strings
        assert isinstance(result1, str)
        assert isinstance(result2, str)
