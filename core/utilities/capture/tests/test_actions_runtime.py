import json
from types import SimpleNamespace

from core.utilities.capture import actions


class _DesktopApi:
    def __init__(self, *, handle=42, switchable=True):
        self.handle = handle
        self.switchable = switchable
        self.closed = []

    def OpenInputDesktop(self, *_args):
        return self.handle

    def SwitchDesktop(self, _handle):
        return self.switchable

    def CloseDesktop(self, handle):
        self.closed.append(handle)


def test_session_state_is_locked_when_secure_desktop_cannot_be_opened(monkeypatch):
    monkeypatch.setattr(actions, "_idle_seconds", lambda: 12.5)
    monkeypatch.setattr(actions, "_user32", _DesktopApi(handle=0))

    assert actions._interactive_session_state() == ("locked", 12.5)


def test_session_state_pauses_before_display_power_transition(monkeypatch):
    api = _DesktopApi()
    monkeypatch.setattr(actions, "_idle_seconds", lambda: 301.0)
    monkeypatch.setattr(actions, "_user32", api)
    monkeypatch.setattr(actions, "IDLE_PAUSE_SECONDS", 300.0)

    assert actions._interactive_session_state() == ("idle", 301.0)
    assert api.closed == [42]


def test_health_file_contains_pid_memory_state_and_last_operation(tmp_path, monkeypatch):
    memory = SimpleNamespace(private=256 * 1024 * 1024, rss=128 * 1024 * 1024)
    monkeypatch.setattr(actions, "LOG_DIR", tmp_path)
    monkeypatch.setattr(actions.psutil, "Process", lambda: SimpleNamespace(memory_info=lambda: memory))
    monkeypatch.setattr(actions.os, "getpid", lambda: 1234)

    actions._write_health(
        state="idle",
        idle_seconds=345.6,
        last_operation="session_state_check",
        last_focus_poll="2026-08-18T10:00:00",
    )

    payload = json.loads((tmp_path / actions.HEALTH_FILENAME).read_text(encoding="utf-8"))
    assert payload["pid"] == 1234
    assert payload["state"] == "idle"
    assert payload["private_memory_mb"] == 256.0
    assert payload["working_set_mb"] == 128.0
    assert payload["last_operation"] == "session_state_check"
