"""Touchless Computer Control System - Acoustic Haptic Audio Feedback Module.

Provides low-latency, non-blocking auditory cues to compensate for the lack of
physical tactile feedback in mid-air spatial gesture interactions.
"""

import sys
import threading
import logging

logger = logging.getLogger("touchless.audio")

# Platform-specific audio backend
_USE_WINSOUND = sys.platform == "win32"
if _USE_WINSOUND:
    try:
        import winsound
    except ImportError:
        _USE_WINSOUND = False


class AudioFeedbackEngine:
    """Non-blocking acoustic haptic sound engine for spatial gesture interfaces."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled and _USE_WINSOUND
        self._lock = threading.Lock()
        self._last_beep_time = 0.0

    def play_click(self):
        """Crisp synthetic snap simulating mechanical switch actuation (1760 Hz, 25ms)."""
        if not self.enabled:
            return
        self._async_beep(frequency=1760, duration_ms=25)

    def play_release(self):
        """Gentle resonant tone on pinch release (440 Hz, 20ms)."""
        if not self.enabled:
            return
        self._async_beep(frequency=440, duration_ms=20)

    def play_mode_switch(self):
        """Two-tone ascending chime for mode or gesture state transitions."""
        if not self.enabled:
            return

        def _chime():
            try:
                winsound.Beep(587, 40)   # D5
                winsound.Beep(880, 60)   # A5
            except Exception as e:
                logger.debug(f"Chime error: {e}")

        threading.Thread(target=_chime, daemon=True).start()

    def _async_beep(self, frequency: int, duration_ms: int):
        """Fires a non-blocking frequency beep in a detached background daemon thread."""
        def _beep():
            try:
                winsound.Beep(int(frequency), int(duration_ms))
            except Exception as e:
                logger.debug(f"Audio playback error: {e}")

        threading.Thread(target=_beep, daemon=True).start()

    def toggle(self, enable: bool = None) -> bool:
        """Toggles audio feedback state."""
        if enable is not None:
            self.enabled = enable and _USE_WINSOUND
        else:
            self.enabled = (not self.enabled) and _USE_WINSOUND
        return self.enabled


# Global singleton instance for easy import across modules
audio_engine = AudioFeedbackEngine(enabled=False)  # Default off until enabled in config

