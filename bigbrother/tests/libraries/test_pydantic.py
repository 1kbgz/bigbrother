from pydantic import BaseModel, Field

from bigbrother import watch

from ..common import create_tester


class MySubModel(BaseModel):
    x: list = []
    y: dict = {}


class MyOtherSubModel(BaseModel):
    x: list = Field(default_factory=list)
    y: dict = Field(default={})


class MyModel(BaseModel):
    a: MySubModel
    b: MyOtherSubModel
    c: MyOtherSubModel = Field(default_factory=MyOtherSubModel)
    d: MySubModel = Field(default=MySubModel())
    e: list = []


class TestPydantic:
    def test_pydantic_setattr(self):
        my_sub_model = MySubModel()
        my_other_sub_model = MyOtherSubModel()
        x = MyModel(a=my_sub_model, b=my_other_sub_model)

        x, called = create_tester(
            instance=x,
            method_name="setitem",
            expected_args=(
                "d",
                my_sub_model,
            ),
            expected_kwargs={},
        )
        x.d = my_sub_model

        assert called[0]
        assert len(called) == 1
        assert x.d == my_sub_model

    def test_pydantic_setattr_sub(self):
        my_sub_model = MySubModel()
        my_other_sub_model = MyOtherSubModel()
        x = MyModel(a=my_sub_model, b=my_other_sub_model)

        called = []

        instance = x.d
        method_name = "setitem"
        expected_args = ("x", [1])
        expected_kwargs = {}

        def track_changes(obj, method, ref, args, kwargs):
            called.append(True)
            print(f"method: {method} args: {args} kwargs: {kwargs}")
            print(type(obj))
            print(type(instance))
            assert obj == instance.__dict__
            assert method == method_name
            assert args == expected_args
            assert kwargs == expected_kwargs

        x = watch(x, track_changes, deepstate=True)

        x.d.x = [1]

        assert called[0]
        assert len(called) == 1
        assert x.d.x == [1]

    def test_pydantic_setattr_deep(self):
        my_sub_model = MySubModel()
        my_other_sub_model = MyOtherSubModel()
        x = MyModel(a=my_sub_model, b=my_other_sub_model)

        called = []

        def track_changes(obj, method, *args, **kwargs):
            called.append(True)
            print(f"method: {method} args: {args} kwargs: {kwargs}")

        x = watch(x, track_changes, deepstate=True)

        x.d.x = [1]
        x.d.x.append(2)
        x.b.y["a"] = 1
        x.e.append(1)

        print(called)
        assert x.d.x == [1, 2]
        assert x.b.y == {"a": 1}
        assert x.e == [1]
        assert all(called)
        assert len(called) == 4
