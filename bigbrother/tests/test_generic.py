from types import SimpleNamespace

from bigbrother import watch


def sample_function():
    pass


def test_objects_that_reject_class_assignment_are_returned_unchanged():
    for obj in (SimpleNamespace(x=1), Exception("x"), sample_function):
        called = []

        watched = watch(obj, lambda *args: called.append(args), deepstate=True)

        assert watched is obj
        assert called == []


def test_deepstate_tracks_parent_mutation_with_unsupported_value():
    called = []
    error = Exception("x")

    watched = watch({}, lambda obj, method, ref, args, kwargs: called.append((method, args)), deepstate=True)
    watched["error"] = error

    assert watched["error"] is error
    assert called == [("setitem", ("error", error))]
