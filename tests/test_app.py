from netflix_dashboard.app import create_app


def test_app_builds_and_callback_runs():
    app = create_app()
    cb = next(iter(app.callback_map.values()))["callback"]
    out = cb.__wrapped__(["Película", "Serie"], "__all__", [2000, 2022])
    assert len(out) == 12 and out[0] != "0"
    empty = cb.__wrapped__([], "__all__", [2000, 2022])
    assert empty[0] == "0"
