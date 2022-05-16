import os
import pytest
from yamllib.env import interpolate
from unittest import mock


ENVVAR_WITHOUT_DEFAULT = "TEST_ENV"
ENVVAR_WITH_DEFAULT = "TEST_ENV:abc"


def format_envvar(field):
    return "${" + field + "}"


def test_interpolate_basic_field():
    result = interpolate("abc")
    assert result == "abc"


def test_interpolate_field_with_defined_envvar_and_no_default():
    with mock.patch.dict(os.environ, {ENVVAR_WITHOUT_DEFAULT: "abc"}):
        result = interpolate(format_envvar(ENVVAR_WITHOUT_DEFAULT))
        assert result == "abc"


def test_interpolate_field_with_undefined_envvar_and_no_default():
    with pytest.raises(EnvironmentError):
        interpolate(format_envvar(ENVVAR_WITHOUT_DEFAULT))


def test_interpolate_field_with_undefined_envvar_and_default():
    result = interpolate(format_envvar(ENVVAR_WITH_DEFAULT))
    assert result == "abc"


def test_interpolate_field_with_defined_envvar_and_default():
    with mock.patch.dict(os.environ, {ENVVAR_WITHOUT_DEFAULT: "def"}):
        result = interpolate(format_envvar(ENVVAR_WITH_DEFAULT))
        assert result == "def"


def test_interpolate_field_with_colons_in_default():
    expected = "http://localhost:9000"
    field = f"{ENVVAR_WITHOUT_DEFAULT}:{expected}"
    result = interpolate(format_envvar(field))
    assert result == expected


def test_interpolate_field_with_multiple_envvars():
    field = "${HOST}:${PORT}"
    with mock.patch.dict(os.environ, {"HOST": "localhost", "PORT": "9000"}):
        result = interpolate(field)
        assert result == "localhost:9000"
