from typing import Iterable, Dict
from copy import deepcopy
import pytest
from yamllib.config import YamlConfig


TEST_FILE = "tests/resources/test_config.yml"
EXPECTED_DICTIONARY = {'config': {'basic': 'abc',
                                  'list': ['abc', 'def', 'ghi'],
                                  'subsection': {'subfield1': True, 'subfield2': 1.23}},
                       'single_field': 123}
NUM_KEYS_TOP_LEVEL = 2
NUM_KEYS_SUBSECTION = 3


def is_secret(config_dict: Dict, secrets: Iterable[str]) -> bool:
    value = config_dict
    for secret in secrets:
        value = value[secret]
    return all(c == "*" for c in value)


config = YamlConfig.load(TEST_FILE)
config_with_secrets = YamlConfig.load(TEST_FILE, secrets=("config.basic", "config.subsection.subfield1"))
config_with_section_secret = YamlConfig.load(TEST_FILE, secrets=("config.subsection",))
frozen_config = YamlConfig.load(TEST_FILE, frozen=True)


# `get` method tests
def test_get_single_key():
    assert config.get('single_field') == 123


def test_get_single_key_not_exists_no_default():
    assert config.get('bad_field') is None


def test_get_single_key_not_exists_default():
    assert config.get('bad_field', default=123) == 123


def test_get_nested_key():
    assert config.get('config', 'basic') == "abc"


def test_get_nested_key_not_exists_no_default():
    assert config.get('config', 'bad_key') is None


def test_get_nested_key_first_key_not_exists_no_default():
    assert config.get('bad_key', 'basic') is None


def test_get_nested_key_not_exists_default():
    assert config.get('config', 'bad_key', default=123) == 123


def test_get_no_keys():
    with pytest.raises(TypeError):
        config.get()


# `to_dict` method tests
def test_to_dict():
    assert config.to_dict() == EXPECTED_DICTIONARY


def test_to_dict_with_secrets():
    config_dict = config_with_secrets.to_dict()
    secret_fields = (["config", "basic",],
                     ["config", "subsection", "subfield1"])
    assert all(is_secret(config_dict, secret) for secret in secret_fields)


def test_to_dict_with_secret_section():
    config_dict = config_with_section_secret.to_dict()
    assert is_secret(config_dict, ('config', 'subsection'))


def test_to_dict_with_secrets_as_kwarg():
    secret = ("config.basic",)
    config_dict = config.to_dict(secrets=secret)
    assert is_secret(config_dict, ('config', 'basic'))


# `frozen` tests on `set` and `del`
def test_frozen_set_raises_error():
    with pytest.raises(AttributeError):
        frozen_config['config'] = "test"


def test_frozen_del_raises_error():
    with pytest.raises(AttributeError):
        del frozen_config['config']


def test_non_frozen_set():
    config_copy = deepcopy(config)
    config_copy['config'] = "abc"
    assert config_copy['config'] == "abc"


def test_non_frozen_del():
    config_copy = deepcopy(config)
    del config_copy['config']
    assert "abc" not in config_copy


# `len` test
def test_len():
    assert len(config) == NUM_KEYS_TOP_LEVEL


def test_len_subsection():
    assert len(config.get('config')) == NUM_KEYS_SUBSECTION


# `iter` test
def test_iter():
    assert sum(1 for _ in iter(config)) == NUM_KEYS_TOP_LEVEL


def test_iter_subsection():
    assert sum(1 for _ in iter(config.get('config'))) == NUM_KEYS_SUBSECTION
