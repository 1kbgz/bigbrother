from pytest import fixture

from ..common import create_tester


@fixture
def a_dict():
    return {1: "a", 2: "b", 3: "c"}


class TestDict:
    def test_dict_clear(self, a_dict):
        instance, called = create_tester(instance=a_dict, method_name="clear", expected_args=(), expected_kwargs={})
        instance.clear()
        assert called[0]
        assert len(called) == 1
        assert instance == {}

    def test_dict_pop(self, a_dict):
        instance, called = create_tester(instance=a_dict, method_name="pop", expected_args=(1,), expected_kwargs={})
        instance.pop(1)
        assert called[0]
        assert len(called) == 1
        assert instance == {2: "b", 3: "c"}

    def test_dict_popitem(self, a_dict):
        instance, called = create_tester(instance=a_dict, method_name="popitem", expected_args=(), expected_kwargs={})
        instance.popitem()
        assert called[0]
        assert len(called) == 1
        assert instance == {1: "a", 2: "b"}

    def test_dict_update(self, a_dict):
        instance, called = create_tester(instance=a_dict, method_name="update", expected_args=({4: "d"},), expected_kwargs={})
        instance.update({4: "d"})
        assert called[0]
        assert len(called) == 1
        assert instance == {1: "a", 2: "b", 3: "c", 4: "d"}

    def test_dict___setitem__(self, a_dict):
        instance, called = create_tester(instance=a_dict, method_name="setitem", expected_args=(1, "x"), expected_kwargs={})
        instance[1] = "x"
        assert called[0]
        assert len(called) == 1
        assert instance == {1: "x", 2: "b", 3: "c"}
