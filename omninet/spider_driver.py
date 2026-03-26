"""
Spider Driver - Jolt Robot Control System
=========================================

Hardware abstraction layer for Jolt, the sovereign jumping spider robot.
Provides servo control, gait patterns, and expressive behaviors.

Sovereign Architect: Justin Neal Thomas Conzet
Protocol: Ω-PRIME v1.3
"""

from __future__ import annotations

import time
import math
import random
from dataclasses import dataclass, field
from typing import Optional, Callable
from enum import Enum


class SpiderError(Exception):
    """Base exception for spider driver errors."""
    pass


class HardwareError(SpiderError):
    """Raised when hardware interaction fails."""
    pass


class PoseError(SpiderError):
    """Raised when pose execution fails."""
    pass


class SpiderMood(Enum):
    """Enumeration of spider mood states."""
    IDLE = "idle"
    CURIOUS = "curious"
    EXCITED = "excited"
    ALERT = "alert"
    STEALTH = "stealth"
    PLAYFUL = "playful"


@dataclass
class Servo:
    """
    Servo motor abstraction.
    
    Represents a single servo with angle control.
    Designed for easy replacement with actual hardware drivers.
    
    Attributes:
        name: Servo identifier
        angle: Current angle in degrees (-90 to 90)
        min_angle: Minimum allowed angle
        max_angle: Maximum allowed angle
        callback: Optional callback for angle changes
    
    Example:
        >>> servo = Servo("L0")
        >>> servo.set(45)
        >>> servo.angle
        45.0
    """
    name: str
    angle: float = 0.0
    min_angle: float = -90.0
    max_angle: float = 90.0
    callback: Optional[Callable[[str, float], None]] = None
    
    def set(self, angle: float) -> float:
        """
        Set servo angle with bounds checking.
        
        Args:
            angle: Target angle in degrees
            
        Returns:
            float: Actual angle set (clamped to bounds)
        """
        self.angle = max(self.min_angle, min(self.max_angle, angle))
        
        # Call hardware callback if set
        if self.callback:
            self.callback(self.name, self.angle)
        
        return self.angle
    
    def reset(self) -> float:
        """Reset servo to center position."""
        return self.set(0.0)


@dataclass
class JoltSpider:
    """
    Jolt - The Sovereign Jumping Spider Robot.
    
    Eight-legged spider robot with expressive behaviors.
    Uses bilateral symmetry for leg control.
    
    Attributes:
        legs: Dictionary of 8 servo motors (L0-L3 left, R0-R3 right)
        pose: Current pose name
        mood: Current mood state
    
    Example:
        >>> spider = JoltSpider()
        >>> spider.crouch()
        >>> spider.pose
        'crouch'
        >>> spider.jump()
        >>> spider.express("curious")
    """
    legs: dict[str, Servo] = field(default_factory=dict)
    pose: str = "idle"
    mood: SpiderMood = SpiderMood.IDLE
    _movement_delay: float = 0.05
    
    def __post_init__(self) -> None:
        """Initialize leg servos if not provided."""
        if not self.legs:
            # Create 8 leg servos (4 left, 4 right)
            self.legs = {
                f"L{i}": Servo(f"L{i}") for i in range(4)
            }
            self.legs.update({
                f"R{i}": Servo(f"R{i}") for i in range(4)
            })
    
    def _apply_to_legs(self, angle_func: Callable[[int, str], float]) -> None:
        """
        Apply angle function to all legs.
        
        Args:
            angle_func: Function taking (leg_index, side) and returning angle
        """
        for i in range(4):
            self.legs[f"L{i}"].set(angle_func(i, "L"))
            self.legs[f"R{i}"].set(angle_func(i, "R"))
        time.sleep(self._movement_delay)
    
    def idle(self) -> None:
        """
        Set idle standing pose.
        
        All legs at neutral position.
        """
        self._apply_to_legs(lambda i, side: 0.0)
        self.pose = "idle"
        self.mood = SpiderMood.IDLE
    
    def crouch(self) -> None:
        """
        Set crouching pose.
        
        Legs pulled in, ready to jump.
        """
        self._apply_to_legs(lambda i, side: -30.0)
        self.pose = "crouch"
    
    def extend(self) -> None:
        """
        Set extended pose.
        
        Legs fully extended outward.
        """
        self._apply_to_legs(lambda i, side: 30.0)
        self.pose = "extend"
    
    def jump(self, power: float = 1.0) -> None:
        """
        Execute a jumping motion.
        
        Combines crouch and extend with power-controlled timing.
        
        Args:
            power: Jump power (0.0-1.5, higher = stronger)
        """
        power = max(0.1, min(1.5, power))
        
        # Crouch phase
        self.crouch()
        time.sleep(0.05 * power)
        
        # Extend/jump phase
        self.extend()
        
        # Hop arc simulation
        t = 0.0
        while t < math.pi:
            hop = math.sin(t) * 20 * power
            for i, name in enumerate(self.legs):
                side = name[0]
                factor = 1 if i % 2 == 0 else -1
                self.legs[name].set(30 + hop * factor * 0.3)
            t += 0.3
            time.sleep(0.02)
        
        # Land in crouch
        self.crouch()
        self.pose = "jump"
        self.mood = SpiderMood.EXCITED
    
    def wiggle(self, count: int = 6) -> None:
        """
        Execute a wiggling motion.
        
        Random leg movements for curious/playful expression.
        
        Args:
            count: Number of wiggle iterations
        """
        for _ in range(count):
            for servo in self.legs.values():
                delta = random.uniform(-15, 15)
                servo.set(servo.angle + delta)
            time.sleep(0.04)
        
        self.mood = SpiderMood.CURIOUS
    
    def wave(self, leg_index: int = 0, side: str = "R") -> None:
        """
        Wave a single leg.
        
        Args:
            leg_index: Which leg (0-3)
            side: Which side ('L' or 'R')
        """
        leg_name = f"{side}{leg_index}"
        if leg_name not in self.legs:
            return
        
        leg = self.legs[leg_name]
        for _ in range(3):
            leg.set(60)
            time.sleep(0.1)
            leg.set(-20)
            time.sleep(0.1)
        
        leg.reset()
        self.mood = SpiderMood.PLAYFUL
    
    def prowl(self) -> None:
        """
        Set stealth prowling pose.
        
        Low stance for silent movement.
        """
        self._apply_to_legs(lambda i, side: -20.0 + (10 if i < 2 else -10))
        self.pose = "prowl"
        self.mood = SpiderMood.STEALTH
    
    def alert(self) -> None:
        """
        Set alert pose.
        
        Front legs raised, ready for action.
        """
        # Front legs up, back legs down
        for i in range(4):
            front_angle = 45.0 if i < 2 else -15.0
            self.legs[f"L{i}"].set(front_angle)
            self.legs[f"R{i}"].set(front_angle)
        
        time.sleep(self._movement_delay)
        self.pose = "alert"
        self.mood = SpiderMood.ALERT
    
    def express(self, mood: str) -> None:
        """
        Express a mood through body language.
        
        Args:
            mood: Mood name ('curious', 'excited', 'alert', 'stealth', etc.)
        """
        mood_map = {
            "curious": self.wiggle,
            "excited": lambda: self.jump(1.2),
            "alert": self.alert,
            "stealth": self.prowl,
            "playful": lambda: self.wave(0, "R"),
            "idle": self.idle
        }
        
        action = mood_map.get(mood.lower(), self.idle)
        action()
    
    def get_state(self) -> dict:
        """
        Get current spider state.
        
        Returns:
            dict: State including pose, mood, and leg positions
        """
        return {
            "pose": self.pose,
            "mood": self.mood.value,
            "legs": {name: servo.angle for name, servo in self.legs.items()}
        }


def create_jolt_with_hardware(callback: Callable[[str, float], None]) -> JoltSpider:
    """
    Create a Jolt spider with hardware callback.
    
    Args:
        callback: Function called for each servo update (name, angle)
        
    Returns:
        JoltSpider: Configured spider instance
    """
    spider = JoltSpider()
    for servo in spider.legs.values():
        servo.callback = callback
    return spider
