import yaml
import json
from collections.abc import MutableMapping
from typing import Dict, Tuple, Any, Iterator
from yamllib.env import interpolate


class YamlConfig(MutableMapping):
    __SECRET: Tuple[str, ...] = tuple()

    def __init__(self, frozen: bool = False, **kwargs):
        self.__frozen = frozen
        self.__store: Dict[str, Any] = dict()
        for key, value in kwargs.items():
            if isinstance(value, dict):
                value = YamlConfig(**value)
            else:
                value = interpolate(value)
            self.__store[key] = value

    def to_dict(self, secrets: Tuple[str, ...] = None, previous_key: str = None) -> Dict:
        secrets = secrets or self.__SECRET
        previous_key = previous_key or ''
        results = dict()
        for key, value in self.__store.items():
            full_key = f"{previous_key}.{key}" if previous_key else key
            if full_key in secrets:
                value = '************'
            elif isinstance(value, YamlConfig):
                value = value.to_dict(secrets=secrets, previous_key=full_key)
            results[key] = value
        return results

    def __repr__(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def load(cls, path: str):
        with open(path, 'r') as f:
            config = yaml.safe_load(f.read())
        return cls(**config)

    def __setitem__(self, key: str, value: Any) -> None:
        if self.__frozen:
            raise AttributeError('Config is frozen. Cannot overwrite fields.')
        self.__store[key] = value
        return

    def __delitem__(self, key: str) -> None:
        if self.__frozen:
            raise AttributeError('Config is frozen. Cannot delete fields.')
        del self.__store[key]
        return

    def __getitem__(self, key: str) -> Any:
        return self.__store[key]

    def __len__(self) -> int:
        return len(self.__store)

    def __iter__(self) -> Iterator[str]:
        return iter(self.__store)

    def get(self, *keys: str, default: Any = None) -> Any:
        """
        Gets a value from the config at the specified key location. Accepts any number of keys as
        non-keyword arguments, which represent nested locations in the config. For example, if the
        config has a section:
        ```
        config:
            a:
                b: value
        ```
        then get('config', 'a', 'b') returns 'value'.

        :param keys:        Keys used to access field values
        :param default:     A default value if the provided key does not exist.
        :return:            the value at the provided key location, or else the default value.
        """
        if len(keys) == 1:
            try:
                return self.__getitem__(keys[0])
            except KeyError:
                return default
        sub_store = self.__store[keys[0]]
        if not sub_store:
            raise KeyError(keys[0])
        return sub_store.get(*keys[1:], default=default)
