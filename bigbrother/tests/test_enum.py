from enum import Enum

from bigbrother import watch


class Color(Enum):
    RED = "red"


def test_enum_is_returned_unchanged():
    called = []

    watched = watch(Color.RED, lambda *args: called.append(args), deepstate=True)

    assert watched is Color.RED
    assert called == []


def test_deepstate_leaves_nested_enum_unchanged():
    called = []

    watched = watch({"color": Color.RED}, lambda *args: called.append(args), deepstate=True)

    assert watched["color"] is Color.RED
    watched["status"] = Color.RED
    assert watched["status"] is Color.RED
    assert len(called) == 1
