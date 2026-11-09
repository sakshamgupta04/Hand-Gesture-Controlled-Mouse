"""Unit tests for the Acoustic Haptic Audio Feedback module."""

import pytest
from src.utils.audio_feedback import AudioFeedbackEngine


def test_audio_engine_initialization():
    engine = AudioFeedbackEngine(enabled=False)
    assert engine.enabled is False

    engine.toggle(True)
    assert isinstance(engine.enabled, bool)


def test_audio_engine_methods_do_not_throw():
    """All sound methods should be non-blocking and safe even if muted or on headless systems."""
    engine = AudioFeedbackEngine(enabled=False)
    # Should safely no-op without exceptions
    engine.play_click()
    engine.play_release()
    engine.play_mode_switch()

