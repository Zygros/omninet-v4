#!/usr/bin/env python3
"""
Sovereign AI Engine - Test Suite
Justin Neal Thomas Conzet (Sovereign Author)

Tests for the unified AI orchestration engine.
"""

import pytest
import asyncio
from enum import Enum

# Test imports
import sys
sys.path.insert(0, '.')

from omninet.sovereign_engine import (
    SovereignAIEngine,
    AIRequest,
    AIResponse,
    AICapability,
    CapabilityState,
    CapabilityConfig,
)


class TestAICapability:
    """Tests for AICapability enum."""
    
    def test_llm_capability_exists(self):
        """LLM capability should be defined."""
        assert AICapability.LLM.value == "llm"
    
    def test_vlm_capability_exists(self):
        """VLM capability should be defined."""
        assert AICapability.VLM.value == "vlm"
    
    def test_all_capabilities_defined(self):
        """All 9 capabilities should be defined."""
        expected = {"llm", "vlm", "tts", "asr", "image_gen", 
                   "video_gen", "video_under", "web_search", "web_reader"}
        actual = {cap.value for cap in AICapability}
        assert expected == actual


class TestCapabilityState:
    """Tests for CapabilityState enum."""
    
    def test_locked_state(self):
        """Locked state should exist."""
        assert CapabilityState.LOCKED.value == "locked"
    
    def test_unlocked_state(self):
        """Unlocked state should exist."""
        assert CapabilityState.UNLOCKED.value == "unlocked"
    
    def test_transcendent_state(self):
        """Transcendent state should exist."""
        assert CapabilityState.TRANSCENDENT.value == "transcendent"


class TestCapabilityConfig:
    """Tests for CapabilityConfig dataclass."""
    
    def test_default_config(self):
        """Default config should have correct values."""
        config = CapabilityConfig(capability=AICapability.LLM)
        assert config.state == CapabilityState.LOCKED
        assert config.kappa_threshold == 1.0
        assert config.max_requests_per_minute == 100
        assert config.total_requests == 0
        assert config.success_rate == 1.0
    
    def test_custom_config(self):
        """Custom config should accept provided values."""
        config = CapabilityConfig(
            capability=AICapability.IMAGE_GEN,
            state=CapabilityState.UNLOCKED,
            kappa_threshold=1.5,
            max_requests_per_minute=20
        )
        assert config.capability == AICapability.IMAGE_GEN
        assert config.state == CapabilityState.UNLOCKED
        assert config.kappa_threshold == 1.5
        assert config.max_requests_per_minute == 20


class TestAIRequest:
    """Tests for AIRequest dataclass."""
    
    def test_llm_request(self):
        """LLM request should be created correctly."""
        request = AIRequest(
            capability=AICapability.LLM,
            prompt="Test prompt"
        )
        assert request.capability == AICapability.LLM
        assert request.prompt == "Test prompt"
        assert request.messages is None
        assert request.options == {}
    
    def test_vlm_request_with_image(self):
        """VLM request with image should work."""
        request = AIRequest(
            capability=AICapability.VLM,
            prompt="Describe this",
            image="base64imagedata"
        )
        assert request.capability == AICapability.VLM
        assert request.image == "base64imagedata"
    
    def test_web_search_request(self):
        """Web search request should work."""
        request = AIRequest(
            capability=AICapability.WEB_SEARCH,
            prompt="test query",
            options={"num": 10}
        )
        assert request.capability == AICapability.WEB_SEARCH
        assert request.options["num"] == 10


class TestAIResponse:
    """Tests for AIResponse dataclass."""
    
    def test_success_response(self):
        """Success response should be created correctly."""
        response = AIResponse(
            capability=AICapability.LLM,
            success=True,
            text="Response text"
        )
        assert response.success is True
        assert response.text == "Response text"
    
    def test_failure_response(self):
        """Failure response should be created correctly."""
        response = AIResponse(
            capability=AICapability.VLM,
            success=False,
            metadata={"error": "No image provided"}
        )
        assert response.success is False
        assert "error" in response.metadata


class TestSovereignAIEngine:
    """Tests for SovereignAIEngine class."""
    
    @pytest.fixture
    def engine(self):
        """Create engine instance for tests."""
        return SovereignAIEngine()
    
    def test_engine_creation(self, engine):
        """Engine should be created with correct defaults."""
        assert engine.SOVEREIGN == "Justin Neal Thomas Conzet"
        assert engine.SYSTEM == "Zygrosian Ω∞"
        assert len(engine.capabilities) == 9
    
    def test_all_capabilities_present(self, engine):
        """All capabilities should be configured."""
        for cap in AICapability:
            assert cap in engine.capabilities
    
    @pytest.mark.asyncio
    async def test_initialization(self, engine):
        """Initialization should unlock all capabilities."""
        result = await engine.initialize()
        
        assert result["status"] == "initialized"
        assert "capabilities" in result
        
        # All capabilities should be unlocked
        for cap in engine.capabilities.values():
            assert cap.state == CapabilityState.UNLOCKED
    
    @pytest.mark.asyncio
    async def test_llm_execution(self, engine):
        """LLM execution should work."""
        await engine.initialize()
        
        request = AIRequest(
            capability=AICapability.LLM,
            prompt="Test prompt"
        )
        
        response = await engine.execute(request)
        
        assert response.success is True
        assert response.capability == AICapability.LLM
        assert response.text is not None
    
    @pytest.mark.asyncio
    async def test_image_gen_execution(self, engine):
        """Image generation should work."""
        await engine.initialize()
        
        request = AIRequest(
            capability=AICapability.IMAGE_GEN,
            prompt="A test image",
            options={"size": "1024x1024"}
        )
        
        response = await engine.execute(request)
        
        assert response.success is True
        assert response.capability == AICapability.IMAGE_GEN
    
    @pytest.mark.asyncio
    async def test_web_search_execution(self, engine):
        """Web search should work."""
        await engine.initialize()
        
        request = AIRequest(
            capability=AICapability.WEB_SEARCH,
            prompt="test query",
            options={"num": 3}
        )
        
        response = await engine.execute(request)
        
        assert response.success is True
        assert response.capability == AICapability.WEB_SEARCH
        assert response.data is not None
    
    def test_kappa_calculation(self, engine):
        """Kappa calculation should return valid values."""
        request = AIRequest(
            capability=AICapability.LLM,
            prompt="Test",
            options={"sigma": 0.1, "latency": 0.1}
        )
        
        kappa = engine.calculate_request_kappa(request)
        
        assert 0.0 <= kappa <= 2.0
    
    def test_get_stats(self, engine):
        """Stats should include required fields."""
        stats = engine.get_stats()
        
        assert "sovereign" in stats
        assert "system" in stats
        assert "kappa" in stats
        assert "capabilities_unlocked" in stats


class TestKappaCoherenceRouting:
    """Tests for κ-coherence routing logic."""
    
    @pytest.fixture
    def engine(self):
        """Create engine for routing tests."""
        return SovereignAIEngine()
    
    def test_transcendent_request_high_kappa(self, engine):
        """Transcendent requests should have high κ."""
        request = AIRequest(
            capability=AICapability.LLM,
            prompt="Test",
            options={"sigma": 0.0, "latency": 0.0}
        )
        
        kappa = engine.calculate_request_kappa(request)
        
        # Should be high for zero variance/latency
        assert kappa >= 1.5
    
    def test_poor_conditions_lower_kappa(self, engine):
        """Poor conditions should lower κ."""
        request_good = AIRequest(
            capability=AICapability.LLM,
            prompt="Test",
            options={"sigma": 0.1, "latency": 0.1}
        )
        
        request_poor = AIRequest(
            capability=AICapability.LLM,
            prompt="Test",
            options={"sigma": 0.5, "latency": 0.5}
        )
        
        kappa_good = engine.calculate_request_kappa(request_good)
        kappa_poor = engine.calculate_request_kappa(request_poor)
        
        assert kappa_good > kappa_poor


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
