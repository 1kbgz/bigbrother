from pytest import fixture

from ..common import create_tester


@fixture
def a_set():
    return {1, 2, 3}


class TestDict:
    def test_set_add(self, a_set):
        instance, called = create_tester(instance=a_set, method_name="add", expected_args=(4,), expected_kwargs={})
        instance.add(4)
        assert called[0]
        assert len(called) == 1
        assert instance == {1, 2, 3, 4}

    def test_set_clear(self, a_set):
        instance, called = create_tester(instance=a_set, method_name="clear", expected_args=(), expected_kwargs={})
        instance.clear()
        assert called[0]
        assert len(called) == 1
        assert instance == set()

    def test_set_difference_update(self, a_set):
        instance, called = create_tester(instance=a_set, method_name="difference_update", expected_args=({1, 2, 4},), expected_kwargs={})
        instance.difference_update({1, 2, 4})
        assert called[0]
        assert len(called) == 1
        assert instance == {3}

    def test_set_discard(self, a_set):
        instance, called = create_tester(instance=a_set, method_name="discard", expected_args=(1,), expected_kwargs={})
        instance.discard(1)
        assert called[0]
        assert len(called) == 1
        assert instance == {2, 3}

    def test_set_intersection_update(self, a_set):
        instance, called = create_tester(instance=a_set, method_name="intersection_update", expected_args=({1, 3},), expected_kwargs={})
        instance.intersection_update({1, 3})
        assert called[0]
        assert len(called) == 1
        assert instance == {1, 3}

    def test_set_remove(self, a_set):
        instance, called = create_tester(instance=a_set, method_name="remove", expected_args=(1,), expected_kwargs={})
        instance.remove(1)
        assert called[0]
        assert len(called) == 1
        assert instance == {2, 3}

    def test_set_symmetric_difference_update(self, a_set):
        instance, called = create_tester(instance=a_set, method_name="intersection_update", expected_args=({1, 3},), expected_kwargs={})
        instance.intersection_update({1, 3})
        assert called[0]
        assert len(called) == 1
        assert instance == {1, 3}

    def test_set_update(self, a_set):
        instance, called = create_tester(instance=a_set, method_name="update", expected_args=({4, 5},), expected_kwargs={})
        instance.update({4, 5})
        assert called[0]
        assert len(called) == 1
        assert instance == {1, 2, 3, 4, 5}
