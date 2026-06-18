from dataclasses import dataclass, field

from bigbrother import watch


@dataclass
class Sub:
    label: str = ""
    tags: list = field(default_factory=list)


@dataclass
class Obj:
    name: str
    on: bool = False
    meta: Sub = field(default_factory=Sub)


class TestDataclass:
    def test_setattr(self):
        o = Obj(name="x")
        called = []
        watch(o, lambda obj, method, ref, args, kwargs: called.append((method, args)), deepstate=True)
        o.on = True
        assert o.on is True
        assert ("setattr", ("on", True)) in called

    def test_nested_model_setattr(self):
        o = Obj(name="x", meta=Sub(label="a"))
        called = []
        watch(o, lambda obj, method, ref, args, kwargs: called.append((method, args)), deepstate=True)
        o.meta.label = "b"
        assert o.meta.label == "b"
        assert ("setattr", ("label", "b")) in called

    def test_nested_list_append(self):
        o = Obj(name="x", meta=Sub(tags=["a"]))
        called = []
        watch(o, lambda obj, method, ref, args, kwargs: called.append((method, args)), deepstate=True)
        o.meta.tags.append("b")
        assert o.meta.tags == ["a", "b"]
        assert any(m == "append" for m, _ in called)

    def test_slots_object_is_returned_unchanged(self):
        # objects without a __dict__ cannot be observed via the __dict__ trick
        class Slotted:
            __slots__ = ("x",)

            def __init__(self):
                self.x = 1

        s = Slotted()
        watched = watch(s, lambda *a, **k: None, deepstate=True)
        assert watched is s  # returned unchanged, no error
