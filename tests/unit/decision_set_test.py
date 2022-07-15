import pytest

from src.decision.decision import Decision
from src.decision.decision_set import DecisionSet
from src.decision.decision_type import DecisionType
from src.object_kind import ObjectKind


@pytest.fixture
def decision_set():
    return DecisionSet()


@pytest.fixture
def decision():
    return Decision(DecisionType.MOVE, kind=ObjectKind.FISH)


def test_add(decision_set, decision):
    decision_set.add(decision)
    assert len(decision_set.decisions.keys()) == 1
    assert len(decision_set.decisions[decision.decision_type].keys()) == 1
    assert len(decision_set.decisions[decision.decision_type][decision.kind]) == 1


def test_add_dunder(decision):
    ds1 = DecisionSet()
    ds1.add(decision)
    ds2 = DecisionSet()
    ds3 = ds1 + ds2

    assert id(ds3) != id(ds2) and id(ds3) != id(ds1)
    assert len(ds3.decisions[decision.decision_type][decision.kind]) == 1


def test_iadd_dunder(decision):
    ds1 = DecisionSet()
    ds1.add(decision)
    ds2 = DecisionSet()
    ds2_id = id(ds2)
    ds2 += ds1

    assert id(ds2) == ds2_id and id(ds2) != id(ds1)
    assert len(ds2.decisions[decision.decision_type][decision.kind]) == 1


def test_getitem_dunder(decision_set, decision):
    decision_set.add(decision)
    assert len(decision_set[decision.decision_type, decision.kind]) == 1
    assert len(decision_set[DecisionType.REPRODUCE, ObjectKind.FISH]) == 0
    assert len(decision_set[DecisionType.MOVE, ObjectKind.WORM]) == 0


def test_cannot_deduce_kind_exception(decision_set):
    decision = Decision(DecisionType.MOVE)
    with pytest.raises(Exception):
        decision_set.add(decision)
