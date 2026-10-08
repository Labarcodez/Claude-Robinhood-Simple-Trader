import os

import supervisor


def test_stale_supervisor_lock_is_recovered(tmp_path, monkeypatch):
    lock = tmp_path / "SUPERVISOR.lock"
    monkeypatch.setattr(supervisor, "LOCK_FILE", lock)
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_text("999999999")
    assert supervisor.acquire_lock()
    assert lock.read_text() == str(os.getpid())
    supervisor.release_lock()
    assert not lock.exists()


def test_build_prompt_contains_automation_cycle():
    prompt = supervisor.build_prompt()
    assert "<SUPERVISOR_CYCLE>" in prompt
    assert "broad multi-pass discovery" in prompt


def test_command_available_for_python():
    assert supervisor._command_available(["python"])
