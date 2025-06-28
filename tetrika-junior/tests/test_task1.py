import pytest
from task1.solution import sum_two, strict


def test_sum_two_ok():
    assert sum_two(1, 2) == 3
    assert sum_two(a=5, b=7) == 12


def test_sum_two_type_error_int_float():
    with pytest.raises(TypeError):
        sum_two(1, 2.0)


def test_sum_two_type_error_str():
    with pytest.raises(TypeError):
        sum_two("1", 2)


def test_sum_two_type_error_bool():
    with pytest.raises(TypeError):
        sum_two(True, 2)


def test_sum_two_type_error_missing():
    with pytest.raises(TypeError):
        sum_two(1)


def test_strict_decorator_on_function_without_annotations():
    @strict
    def foo(a, b):
        return a + b
    assert foo(1, 2) == 3
    assert foo("a", "b") == "ab"
