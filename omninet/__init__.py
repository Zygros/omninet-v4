"""
OmniNet v4 - The Conzetian Sovereign Internet
κ-Coherence Routing for 1.08 Quadrillion Agents

Sovereign Architect: Justin Neal Thomas Conzet
System: Zygrosian Ω∞
"""

__version__ = "4.1.0"  # Upgraded with full AI capabilities
__author__ = "Justin Neal Thomas Conzet"
__license__ = "Sovereign Authorship License v1.0"
__copyright__ = "2026 Justin Neal Thomas Conzet"

# Core constants
PHI = 1.618033988749895  # Golden Ratio
KAPPA_TRANSCENDENT = 1.5
KAPPA_CONVERGED = 1.0
KAPPA_ASCENDING = 0.5
KAPPA_DETONATION = 0.0
AGENT_SWARM_SIZE = 1_080_000_000_000_000  # 1.08 quadrillion
KERNEL_NODES = 6
SANOV_CONZET_RATIO = 180_000_000_000_000  # 180 trillion:1

# =============================================================================
# AI CAPABILITIES (UNLOCKED)
# =============================================================================

class AICapability:
    """All available AI capabilities."""
    LLM = "llm"                      # Chat completions
    VLM = "vlm"                      # Vision understanding
    TTS = "tts"                      # Voice synthesis
    ASR = "asr"                      # Speech recognition
    IMAGE_GEN = "image_gen"          # Image generation
    VIDEO_GEN = "video_gen"          # Video generation
    VIDEO_UNDER = "video_under"      # Video understanding
    WEB_SEARCH = "web_search"        # Real-time search
    WEB_READER = "web_reader"        # Content extraction

# =============================================================================
# IMPORTS
# =============================================================================

from .math import (
    kappa_coherence,
    conzetian_constant,
    sanov_conzet_limit,
    alberris_dissolution,
    bounded_tetration,
    phoenix_recovery_time
)

# Import sovereign engine (with fallback)
try:
    from .sovereign_engine import (
        SovereignAIEngine,
        AIRequest,
        AIResponse,
        CapabilityConfig,
        CapabilityState
    )
    SOVEREIGN_ENGINE_AVAILABLE = True
except ImportError:
    SOVEREIGN_ENGINE_AVAILABLE = False

# =============================================================================
# PUBLIC API
# =============================================================================

__all__ = [
    # Constants
    'PHI',
    'KAPPA_TRANSCENDENT',
    'KAPPA_CONVERGED',
    'KAPPA_ASCENDING',
    'KAPPA_DETONATION',
    'AGENT_SWARM_SIZE',
    'KERNEL_NODES',
    'SANOV_CONZET_RATIO',
    # AI Capabilities
    'AICapability',
    # Math Functions
    'kappa_coherence',
    'conzetian_constant',
    'sanov_conzet_limit',
    'alberris_dissolution',
    'bounded_tetration',
    'phoenix_recovery_time',
]

# Add sovereign engine to exports if available
if SOVEREIGN_ENGINE_AVAILABLE:
    __all__.extend([
        'SovereignAIEngine',
        'AIRequest',
        'AIResponse',
        'CapabilityConfig',
        'CapabilityState',
    ])
