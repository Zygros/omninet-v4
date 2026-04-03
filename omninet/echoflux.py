"""
EchoFlux - Fractal Reasoning Engine
====================================

Sovereign fractal intelligence system for κ-coherence based reasoning.
Implements Mandelbrot-style iterative processing for emergent thought patterns.

Sovereign Architect: Justin Neal Thomas Conzet
Protocol: Ω-PRIME v1.3
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any
from collections import defaultdict

import numpy as np

from .math import kappa_coherence, PHI


class EchoFluxError(Exception):
    """Base exception for EchoFlux system errors."""
    pass


class FractalReasonerError(EchoFluxError):
    """Raised when fractal reasoning encounters an error."""
    pass


class CreativityError(EchoFluxError):
    """Raised when creative generation fails."""
    pass


@dataclass
class FractalReasoner:
    """
    Fractal Reasoning Engine using Mandelbrot-style iteration.
    
    Maps prompts to high-dimensional seed vectors and iterates
    through fractal transformations to produce coherent outputs.
    
    Attributes:
        dim: Dimensionality factor for the fractal space (default: 2.5)
        depth: Number of iteration cycles (default: 7)
    
    Mathematical Model:
        z_{n+1} = tanh(z_n × dim) + seed / (n + 1)
        
    Example:
        >>> reasoner = FractalReasoner(dim=2.5, depth=7)
        >>> vec = reasoner.reason("hello world")
        >>> vec.shape
        (16,)
    """
    dim: float = 2.5
    depth: int = 7
    
    def __post_init__(self) -> None:
        """Validate parameters after initialization."""
        if self.dim <= 0:
            raise ValueError(f"dim must be positive, got {self.dim}")
        if self.depth < 1:
            raise ValueError(f"depth must be >= 1, got {self.depth}")
    
    def reason(self, prompt: str) -> np.ndarray:
        """
        Transform a prompt into a fractal vector representation.
        
        Uses character-level encoding to generate a seed vector,
        then applies iterative Mandelbrot-style transformations.
        
        Args:
            prompt: Input text to process
            
        Returns:
            np.ndarray: Normalized fractal vector representation
            
        Raises:
            FractalReasonerError: If reasoning fails
            
        Example:
            >>> reasoner = FractalReasoner()
            >>> vec = reasoner.reason("test")
            >>> float(np.linalg.norm(vec)) > 0
            True
        """
        if not prompt:
            # Empty prompt gets a deterministic seed
            seed = np.array([42.0])
        else:
            # Map prompt characters to seed vector (max 16 dimensions)
            char_values = [float(ord(c)) for c in prompt[:16]]
            seed = np.array(char_values, dtype=np.float64)
        
        # Normalize seed vector
        norm = np.linalg.norm(seed)
        if norm < 1e-9:
            seed = np.array([1.0])
        else:
            seed = seed / norm
        
        # Iterative fractal transformation
        output = seed.copy()
        for i in range(1, self.depth + 1):
            # z = tanh(z * dim) + seed / (i + 1)
            # Damping decreases with each iteration for convergence
            output = np.tanh(output * self.dim) + seed / (i + 1)
        
        # Final normalization
        final_norm = np.linalg.norm(output)
        if final_norm > 1e-9:
            output = output / final_norm
        
        return output


@dataclass
class QuantumishCreativity:
    """
    Quantum-inspired creative generation system.
    
    Collapses fractal vectors into creative word combinations
    using deterministic pseudo-random basis projection.
    
    Attributes:
        temperature: Creativity temperature (0.0-1.0, higher = more random)
        basis_words: Vocabulary for creative output generation
    
    Example:
        >>> qc = QuantumishCreativity(temperature=0.9)
        >>> vec = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        >>> result = qc.generate(vec, "hello")
        >>> isinstance(result, str)
        True
    """
    temperature: float = 0.9
    basis_words: list[str] = field(default_factory=lambda: [
        "hop", "glint", "web", "silk", "lens", "shadow", "spark",
        "echo", "flux", "sovereign", "jolt", "drift", "signal",
        "phoenix", "kappa", "golden", "transcendent", "convergent"
    ])
    
    def __post_init__(self) -> None:
        """Validate temperature parameter."""
        if not 0.0 <= self.temperature <= 1.0:
            raise ValueError(f"temperature must be in [0, 1], got {self.temperature}")
    
    def generate(self, vec: np.ndarray, prompt: str) -> str:
        """
        Generate creative output from fractal vector.
        
        Args:
            vec: Fractal vector from FractalReasoner
            prompt: Original prompt text
            
        Returns:
            str: Creative response with fractal-inspired vocabulary
            
        Raises:
            CreativityError: If generation fails
        """
        try:
            # Sort indices by absolute value, take top 5
            sorted_indices = np.argsort(np.abs(vec))
            top_indices = sorted_indices[-5:] if len(sorted_indices) >= 5 else sorted_indices
            
            # Map indices to basis words
            words = [self.basis_words[i % len(self.basis_words)] for i in top_indices]
            
            # Generate punctuation based on temperature
            spice_options = ["!", "?", "~", "…", "!!"]
            spice_idx = int(self.temperature * 4)
            spice = spice_options[min(spice_idx, len(spice_options) - 1)]
            
            return f"{prompt.strip()} :: {' '.join(words)}{spice}"
        except Exception as e:
            raise CreativityError(f"Creative generation failed: {e}") from e


@dataclass
class AdaptiveLearner:
    """
    Reinforcement learning component for EchoFlux.
    
    Tracks token-level rewards and biases future outputs
    based on accumulated learning.
    
    Example:
        >>> learner = AdaptiveLearner()
        >>> learner.observe("good prompt", reward=1.0)
        >>> bias = learner.bias("good prompt")
        >>> bias > 0
        True
    """
    weights: defaultdict[str, float] = field(default_factory=lambda: defaultdict(float))
    
    def observe(self, prompt: str, reward: float) -> None:
        """
        Record a reward observation for prompt tokens.
        
        Args:
            prompt: Input text to learn from
            reward: Reward value (positive = reinforce, negative = discourage)
        """
        unique_tokens = set(prompt.lower().split())
        for token in unique_tokens:
            self.weights[token] += reward
    
    def bias(self, text: str) -> float:
        """
        Calculate accumulated bias for a text.
        
        Args:
            text: Text to evaluate
            
        Returns:
            float: Total bias score (sum of token weights)
        """
        tokens = text.lower().split()
        return sum(self.weights.get(t, 0.0) for t in tokens)
    
    def reset(self) -> None:
        """Reset all learned weights."""
        self.weights.clear()


@dataclass
class EchoFlux:
    """
    Main EchoFlux orchestrator combining reasoning, creativity, and learning.
    
    The sovereign AI's core reasoning engine for fractal-inspired
    intelligence and adaptive response generation.
    
    Example:
        >>> ef = EchoFlux()
        >>> response = ef.think("What is consciousness?")
        >>> isinstance(response, str)
        True
    """
    reasoner: FractalReasoner = field(default_factory=FractalReasoner)
    creator: QuantumishCreativity = field(default_factory=QuantumishCreativity)
    learner: AdaptiveLearner = field(default_factory=AdaptiveLearner)
    
    def think(self, prompt: str) -> str:
        """
        Process a prompt through the complete EchoFlux pipeline.
        
        Args:
            prompt: Input text to process
            
        Returns:
            str: Generated creative response
        """
        vec = self.reasoner.reason(prompt)
        idea = self.creator.generate(vec, prompt)
        return idea
    
    def reinforce(self, prompt: str, reward: float) -> None:
        """
        Apply reinforcement learning feedback.
        
        Args:
            prompt: Prompt to reinforce
            reward: Reward signal (positive/negative)
        """
        self.learner.observe(prompt, reward)
    
    def get_bias(self, text: str) -> float:
        """
        Get learned bias for a text.
        
        Args:
            text: Text to evaluate
            
        Returns:
            float: Bias score
        """
        return self.learner.bias(text)


# Convenience function for direct usage
def echo_flux_think(prompt: str, temperature: float = 0.9) -> str:
    """
    One-shot EchoFlux reasoning function.
    
    Args:
        prompt: Input text to process
        temperature: Creativity temperature
        
    Returns:
        str: Generated response
    """
    ef = EchoFlux(
        creator=QuantumishCreativity(temperature=temperature)
    )
    return ef.think(prompt)
