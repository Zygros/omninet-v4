"""
Tests for Spider Driver Module
==============================

Comprehensive test suite for JoltSpider, Servo,
and spider robot control functionality.
"""

import pytest

from omninet.spider_driver import (
    JoltSpider,
    Servo,
    SpiderMood,
    SpiderError,
    create_jolt_with_hardware,
)


class TestServo:
    """Test suite for Servo class."""

    def test_init_defaults(self):
        """Test default initialization."""
        servo = Servo("test")
        assert servo.name == "test"
        assert servo.angle == 0.0
        assert servo.min_angle == -90.0
        assert servo.max_angle == 90.0

    def test_set_angle(self):
        """Test setting angle."""
        servo = Servo("test")
        result = servo.set(45.0)
        assert result == 45.0
        assert servo.angle == 45.0

    def test_set_clamps_high(self):
        """Test that high angles are clamped."""
        servo = Servo("test")
        result = servo.set(100.0)
        assert result == 90.0
        assert servo.angle == 90.0

    def test_set_clamps_low(self):
        """Test that low angles are clamped."""
        servo = Servo("test")
        result = servo.set(-100.0)
        assert result == -90.0
        assert servo.angle == -90.0

    def test_reset(self):
        """Test reset to center."""
        servo = Servo("test")
        servo.set(45.0)
        result = servo.reset()
        assert result == 0.0
        assert servo.angle == 0.0

    def test_callback_called(self):
        """Test that callback is called on set."""
        calls = []
        def callback(name, angle):
            calls.append((name, angle))
        
        servo = Servo("test", callback=callback)
        servo.set(30.0)
        
        assert len(calls) == 1
        assert calls[0] == ("test", 30.0)


class TestJoltSpider:
    """Test suite for JoltSpider class."""

    def test_init_defaults(self):
        """Test default initialization."""
        spider = JoltSpider()
        assert len(spider.legs) == 8
        assert spider.pose == "idle"
        assert spider.mood == SpiderMood.IDLE

    def test_legs_created(self):
        """Test that all legs are created."""
        spider = JoltSpider()
        # Should have L0-L3 and R0-R3
        for i in range(4):
            assert f"L{i}" in spider.legs
            assert f"R{i}" in spider.legs

    def test_idle_pose(self):
        """Test idle pose."""
        spider = JoltSpider()
        spider.idle()
        assert spider.pose == "idle"
        assert spider.mood == SpiderMood.IDLE
        for servo in spider.legs.values():
            assert servo.angle == 0.0

    def test_crouch_pose(self):
        """Test crouch pose."""
        spider = JoltSpider()
        spider.crouch()
        assert spider.pose == "crouch"
        for servo in spider.legs.values():
            assert servo.angle == -30.0

    def test_extend_pose(self):
        """Test extend pose."""
        spider = JoltSpider()
        spider.extend()
        assert spider.pose == "extend"
        for servo in spider.legs.values():
            assert servo.angle == 30.0

    def test_jump(self):
        """Test jump motion."""
        spider = JoltSpider()
        spider.jump(power=1.0)
        assert spider.pose == "jump"
        assert spider.mood == SpiderMood.EXCITED

    def test_wiggle(self):
        """Test wiggle motion."""
        spider = JoltSpider()
        spider.wiggle()
        assert spider.mood == SpiderMood.CURIOUS

    def test_alert_pose(self):
        """Test alert pose."""
        spider = JoltSpider()
        spider.alert()
        assert spider.pose == "alert"
        assert spider.mood == SpiderMood.ALERT

    def test_prowl_pose(self):
        """Test prowl pose."""
        spider = JoltSpider()
        spider.prowl()
        assert spider.pose == "prowl"
        assert spider.mood == SpiderMood.STEALTH

    def test_express_curious(self):
        """Test expressing curious mood."""
        spider = JoltSpider()
        spider.express("curious")
        assert spider.mood == SpiderMood.CURIOUS

    def test_express_excited(self):
        """Test expressing excited mood."""
        spider = JoltSpider()
        spider.express("excited")
        assert spider.mood == SpiderMood.EXCITED

    def test_express_alert(self):
        """Test expressing alert mood."""
        spider = JoltSpider()
        spider.express("alert")
        assert spider.mood == SpiderMood.ALERT

    def test_express_stealth(self):
        """Test expressing stealth mood."""
        spider = JoltSpider()
        spider.express("stealth")
        assert spider.mood == SpiderMood.STEALTH

    def test_express_unknown_defaults_to_idle(self):
        """Test that unknown mood defaults to idle."""
        spider = JoltSpider()
        spider.express("unknown_mood")
        assert spider.mood == SpiderMood.IDLE

    def test_get_state(self):
        """Test getting spider state."""
        spider = JoltSpider()
        state = spider.get_state()
        assert "pose" in state
        assert "mood" in state
        assert "legs" in state
        assert isinstance(state["legs"], dict)

    def test_wave(self):
        """Test wave motion."""
        spider = JoltSpider()
        spider.wave(0, "R")
        assert spider.mood == SpiderMood.PLAYFUL

    def test_jump_power_clamping(self):
        """Test that jump power is clamped."""
        spider = JoltSpider()
        # Very high power
        spider.jump(power=10.0)
        assert spider.mood == SpiderMood.EXCITED
        
        # Very low power
        spider.jump(power=0.01)
        assert spider.mood == SpiderMood.EXCITED


class TestSpiderMood:
    """Test suite for SpiderMood enum."""

    def test_values(self):
        """Test enum values."""
        assert SpiderMood.IDLE.value == "idle"
        assert SpiderMood.CURIOUS.value == "curious"
        assert SpiderMood.EXCITED.value == "excited"
        assert SpiderMood.ALERT.value == "alert"
        assert SpiderMood.STEALTH.value == "stealth"
        assert SpiderMood.PLAYFUL.value == "playful"


class TestCreateJoltWithHardware:
    """Test suite for hardware callback integration."""

    def test_creates_spider_with_callback(self):
        """Test creating spider with hardware callback."""
        calls = []
        def callback(name, angle):
            calls.append((name, angle))
        
        spider = create_jolt_with_hardware(callback)
        
        # Test that callback works
        spider.idle()
        assert len(calls) == 8  # One call per leg
