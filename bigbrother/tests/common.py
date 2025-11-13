from pydantic import BaseModel

from bigbrother import watch


def create_tester(instance, method_name, expected_ref=None, expected_args=None, expected_kwargs=None):
    called = []
    expected_ref = expected_ref or instance
    expected_args = expected_args or ()
    expected_kwargs = expected_kwargs or {}

    def track_changes(obj, method, ref, args, kwargs):
        called.append(True)
        print(f"method: {method} args: {args} kwargs: {kwargs}")
        print(f"ref: {ref} expected_ref: {expected_ref}")
        print(f"obj: {obj} instance: {instance}")
        print(f"type obj: {type(obj)} type instance: {type(instance)}")
        if isinstance(instance, BaseModel):
            assert obj == instance.__dict__
        else:
            assert obj == instance
        assert ref == expected_ref
        assert method == method_name
        assert args == expected_args
        assert kwargs == expected_kwargs

    return watch(instance, track_changes), called
