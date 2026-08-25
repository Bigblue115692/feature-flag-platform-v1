from types import SimpleNamespace
from backend.app.evaluation import evaluate_flag, stable_bucket
from backend.app.schemas import UserContext


def flag(**overrides):
    data = {
        "key": "test",
        "enabled": True,
        "premium_only": False,
        "rollout_percentage": 100.0,
        "targeting_rules": [],
    }
    data.update(overrides)
    return SimpleNamespace(**data)


def test_bucket_stable():
    a = stable_bucket("p", "e", "f", "u")
    b = stable_bucket("p", "e", "f", "u")
    assert a == b
    assert 0 <= a < 10_000


def test_disabled():
    result = evaluate_flag("p", "e", flag(enabled=False), UserContext(id="u"))
    assert result.enabled is False
    assert result.reason == "flag_disabled"


def test_premium_only():
    result = evaluate_flag("p", "e", flag(premium_only=True), UserContext(id="u", premium=False))
    assert result.enabled is False
    assert result.reason == "premium_required"


def test_targeting_match():
    result = evaluate_flag(
        "p",
        "e",
        flag(targeting_rules=[{"attribute": "country", "operator": "equals", "value": "US"}]),
        UserContext(id="u", attributes={"country": "US"}),
    )
    assert result.enabled is True
