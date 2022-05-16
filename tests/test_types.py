from yamllib.types import cast
import pytest

def test_cast_string():
    value = cast("abc")
    assert value == "abc"


def test_cast_string_uppercase():
    value = cast("ABC")
    assert value == "ABC"


def test_cast_boolean():
    value = cast("true")
    assert value is True


def test_cast_boolean_mixed_case():
    value = cast("tRuE")
    assert value is True


def test_cast_boolean_false():
    value = cast("false")
    assert value is False


def test_cast_bad_boolean():
    value = cast("t")
    assert value == "t"


def test_cast_int():
    value = cast("123")
    assert value == 123


def test_cast_float():
    value = cast("1.23")
    assert value == 1.23


def test_cast_list_string():
    value = cast("a,b,c")
    assert value == ["a", "b", "c"]


def test_cast_list_bool():
    value = cast("true,True,FALSE")
    assert value == [True, True, False]


def test_cast_list_int():
    value = cast("1,2,3")
    assert value == [1, 2, 3]


def test_cast_list_float():
    value = cast("1.23,4.56,7.89")
    assert value == [1.23, 4.56, 7.89]


def test_cast_mixed_list():
    value = cast("abc,123,1.23,true")
    assert value == ["abc", 123, 1.23, True]


def test_cast_empty_list():
    value = cast(list())
    assert value is None
