from pytest import fixture

from ..common import create_tester


@fixture
def a_list():
    return [1, 2, 3]


class TestList:
    def test_list_append(self, a_list):
        instance, called = create_tester(instance=a_list, method_name="append", expected_args=(1,), expected_kwargs={})
        instance.append(1)
        assert called[0]
        assert len(called) == 1
        assert instance == [1, 2, 3, 1]

    def test_list_clear(self, a_list):
        instance, called = create_tester(instance=a_list, method_name="clear", expected_args=(), expected_kwargs={})
        instance.clear()
        assert called[0]
        assert len(called) == 1
        assert instance == []

    def test_list_extend(self, a_list):
        instance, called = create_tester(instance=a_list, method_name="extend", expected_args=([1, 2, 3],), expected_kwargs={})
        instance.extend([1, 2, 3])
        assert called[0]
        assert len(called) == 1
        assert instance == [1, 2, 3, 1, 2, 3]

    def test_list_insert(self, a_list):
        instance, called = create_tester(
            instance=a_list,
            method_name="insert",
            expected_args=(
                0,
                1,
            ),
            expected_kwargs={},
        )
        instance.insert(0, 1)
        assert called[0]
        assert len(called) == 1
        assert instance == [1, 1, 2, 3]

    def test_list_pop(self, a_list):
        instance, called = create_tester(instance=a_list, method_name="pop", expected_args=(0,), expected_kwargs={})
        instance.pop(0)
        assert called[0]
        assert len(called) == 1
        assert instance == [2, 3]

    def test_list_remove(self, a_list):
        instance, called = create_tester(instance=a_list, method_name="remove", expected_args=(1,), expected_kwargs={})
        instance.remove(1)
        assert called[0]
        assert len(called) == 1
        assert instance == [2, 3]

    def test_list_sort(self, a_list):
        instance, called = create_tester(instance=a_list, method_name="sort", expected_args=(), expected_kwargs={})
        instance.sort()
        assert called[0]
        assert len(called) == 1
        assert instance == [1, 2, 3]

    def test_list___setitem__(self, a_list):
        instance, called = create_tester(instance=a_list, method_name="setitem", expected_args=(1, 4), expected_kwargs={})
        instance[1] = 4
        assert called[0]
        assert len(called) == 1
        assert instance == [1, 4, 3]
