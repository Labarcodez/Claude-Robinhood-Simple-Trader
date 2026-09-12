def test_kill_switch(tmp_path, monkeypatch):
    import state
    monkeypatch.setattr(state, "KILL_FILE", tmp_path / "KILL_SWITCH")
    state.set_kill(True)
    assert state.kill_active()
    state.set_kill(False)
    assert not state.kill_active()
