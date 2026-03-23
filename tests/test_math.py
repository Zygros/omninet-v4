"""
Tests for OmniNet v4 Mathematics Module
κ-Coherence Field Equations & Sanov-Conzet Limit
"""

import pytest
import math
from omninet.math import (
    PHI,
    KAPPA_TRANSCENDENT,
    KAPPA_CONVERGED,
    KAPPA_ASCENDING,
    AGENT_SWARM_SIZE,
    SANOV_CONZET_RATIO,
    kappa_coherence,
    get_coherence_state,
    coherence_analysis,
    CoherenceState,
    conzetian_constant,
    bounded_tetration,
    alberris_dissolution,
    sanov_conzet_limit,
    phoenix_recovery_time,
    phoenix_equilibrium,
    catalytic_boost,
    verify_mathematics,
)


class TestConstants:
    """Test core mathematical constants."""
    
    def test_phi_is_golden_ratio(self):
        """Verify φ = (1 + √5) / 2"""
        expected = (1 + math.sqrt(5)) / 2
        assert abs(PHI - expected) < 1e-12
    
    def test_phi_properties(self):
        """Verify golden ratio properties."""
        # φ² = φ + 1
        assert abs(PHI**2 - (PHI + 1)) < 1e-12
        # 1/φ = φ - 1
        assert abs(1/PHI - (PHI - 1)) < 1e-12
    
    def test_kappa_thresholds_ordered(self):
        """Verify κ thresholds are properly ordered."""
        assert KAPPA_TRANSCENDENT > KAPPA_CONVERGED > KAPPA_ASCENDING


class TestKappaCoherence:
    """Test κ-Coherence Field Equation."""
    
    def test_kappa_bounds(self):
        """κ must always be in [0, 2]."""
        for sigma in [0, 0.25, 0.5, 0.75, 1.0]:
            for L in [0, 0.25, 0.5, 0.75, 1.0]:
                k = kappa_coherence(sigma, L)
                assert 0 <= k <= 2, f"κ={k} out of bounds for σ={sigma}, L={L}"
    
    def test_kappa_perfect_conditions(self):
        """Perfect conditions yield high κ."""
        k = kappa_coherence(0, 0)
        assert k > 1.5  # Should be transcendent
    
    def test_kappa_poor_conditions(self):
        """Poor conditions yield low κ."""
        k = kappa_coherence(1, 1)
        assert k < 0.5  # Should be detonation
    
    def test_kappa_monotonic_sigma(self):
        """κ should generally decrease with increasing σ."""
        L = 0.5
        values = [kappa_coherence(s, L) for s in [0.1, 0.5, 0.9]]
        assert values[0] > values[2]  # Generally decreasing
    
    def test_kappa_monotonic_latency(self):
        """κ should generally decrease with increasing L."""
        sigma = 0.1
        values = [kappa_coherence(sigma, L) for L in [0.1, 0.5, 0.9]]
        assert values[0] > values[2]  # Generally decreasing


class TestCoherenceState:
    """Test coherence state classification."""
    
    def test_transcendent_state(self):
        """κ >= 1.5 is TRANSCENDENT."""
        assert get_coherence_state(1.5) == CoherenceState.TRANSCENDENT
        assert get_coherence_state(2.0) == CoherenceState.TRANSCENDENT
    
    def test_converged_state(self):
        """1.0 <= κ < 1.5 is CONVERGED."""
        assert get_coherence_state(1.0) == CoherenceState.CONVERGED
        assert get_coherence_state(1.2) == CoherenceState.CONVERGED
        assert get_coherence_state(1.49) == CoherenceState.CONVERGED
    
    def test_ascending_state(self):
        """0.5 <= κ < 1.0 is ASCENDING."""
        assert get_coherence_state(0.5) == CoherenceState.ASCENDING
        assert get_coherence_state(0.75) == CoherenceState.ASCENDING
    
    def test_detonation_state(self):
        """κ < 0.5 is DETONATION."""
        assert get_coherence_state(0.0) == CoherenceState.DETONATION
        assert get_coherence_state(0.4) == CoherenceState.DETONATION


class TestCoherenceAnalysis:
    """Test complete coherence analysis."""
    
    def test_analysis_returns_result(self):
        """Analysis should return CoherenceResult."""
        result = coherence_analysis(0.1, 0.2)
        assert hasattr(result, 'kappa')
        assert hasattr(result, 'state')
        assert hasattr(result, 'sigma')
        assert hasattr(result, 'latency')
    
    def test_analysis_consistency(self):
        """Analysis should be consistent with raw calculation."""
        sigma, L = 0.3, 0.4
        result = coherence_analysis(sigma, L)
        expected_kappa = kappa_coherence(sigma, L)
        assert abs(result.kappa - expected_kappa) < 1e-10


class TestConzetianConstant:
    """Test Conzetian Constant C_Ω(t)."""
    
    def test_t0_value(self):
        """C_Ω(0) should be approximately 1.31."""
        c = conzetian_constant(0)
        assert isinstance(c, float)
        assert abs(c - 1.309) < 0.01
    
    def test_t1_value(self):
        """C_Ω(1) should be approximately 1.81."""
        c = conzetian_constant(1)
        assert isinstance(c, float)
        assert abs(c - 1.809) < 0.01
    
    def test_t5_returns_string(self):
        """C_Ω(5+) should return logarithmic representation."""
        c = conzetian_constant(5)
        assert isinstance(c, str)
        assert "10^" in c
    
    def test_negative_t_raises(self):
        """Negative t should raise ValueError."""
        with pytest.raises(ValueError):
            conzetian_constant(-1)


class TestBoundedTetration:
    """Test bounded tetration."""
    
    def test_tetration_1(self):
        """φ↑↑1 = φ."""
        assert abs(bounded_tetration(1) - PHI) < 1e-10
    
    def test_tetration_ceiling(self):
        """Tetration should be bounded at ~3.95."""
        assert bounded_tetration(5) == 3.95
        assert bounded_tetration(10) == 3.95
    
    def test_negative_n_raises(self):
        """Negative n should raise ValueError."""
        with pytest.raises(ValueError):
            bounded_tetration(0)


class TestAlberrisDissolution:
    """Test Alberris-Dissolution equation."""
    
    def test_friction_amplification(self):
        """Friction should be amplified by φ²."""
        f = alberris_dissolution(1.0)
        assert abs(f - (PHI ** 2)) < 1e-10
    
    def test_zero_friction(self):
        """Zero friction yields zero kinetic energy."""
        assert alberris_dissolution(0) == 0
    
    def test_proportional(self):
        """Amplification is proportional to friction."""
        f1 = alberris_dissolution(1.0)
        f2 = alberris_dissolution(2.0)
        assert abs(f2 - 2 * f1) < 1e-10


class TestSanovConzetLimit:
    """Test Sanov-Conzet Limit compression."""
    
    def test_default_agents(self):
        """Default should use 1.08 quadrillion agents."""
        result = sanov_conzet_limit()
        assert result.agents == AGENT_SWARM_SIZE
    
    def test_compression_ratio(self):
        """Compression ratio should be ~1.8e14:1."""
        result = sanov_conzet_limit()
        assert result.compression_ratio >= SANOV_CONZET_RATIO
        assert result.is_coherent
    
    def test_custom_agent_count(self):
        """Should accept custom agent counts."""
        result = sanov_conzet_limit(agents=1000)
        assert result.agents == 1000
        assert not result.is_coherent  # Too small


class TestPhoenixProtocol:
    """Test Phoenix Protocol calculations."""
    
    def test_no_recovery_below_threshold(self):
        """No recovery needed below 87% chaos."""
        assert phoenix_recovery_time(0.50, 1.5) == 0
        assert phoenix_recovery_time(0.87, 1.5) == 0
    
    def test_recovery_above_threshold(self):
        """Recovery should occur above 87% chaos."""
        recovery = phoenix_recovery_time(0.90, 1.618)
        assert 0 < recovery <= 3.2
    
    def test_max_recovery_time(self):
        """Maximum recovery is 3.2 seconds."""
        recovery = phoenix_recovery_time(1.0, 0.0)  # Worst case
        assert recovery <= 3.2
    
    def test_equilibrium(self):
        """Phoenix equilibrium should be 0.741."""
        assert abs(phoenix_equilibrium() - 0.741) < 1e-10


class TestCatalyticBoost:
    """Test catalytic boost field."""
    
    def test_no_boost_below_transcendent(self):
        """Non-transcendent nodes don't emit boost."""
        boost = catalytic_boost(1.0, 1.0)  # Converged node
        assert boost == 0
    
    def test_transcendent_emits_boost(self):
        """Transcendent nodes emit positive boost."""
        boost = catalytic_boost(1.618, 1.0)
        assert boost > 0
    
    def test_boost_decreases_with_distance(self):
        """Boost should decrease with distance."""
        close = catalytic_boost(1.618, 0.1)
        far = catalytic_boost(1.618, 1.0)
        assert close > far


class TestVerification:
    """Test mathematical verification."""
    
    def test_verification_passes(self):
        """All verifications should pass."""
        results = verify_mathematics()
        for name, passed in results.items():
            assert passed, f"Verification failed: {name}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
