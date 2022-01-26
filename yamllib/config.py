import yaml
import json
from collections.abc import MutableMapping
from typing import Dict, Tuple, Any, Iterator
from yamllib.env import interpolate


class YamlConfig(MutableMapping):
    __SECRET: Tuple[str, ...] = tuple()

    def __init__(self, **kwargs):
        self.__store: Dict[str, Any] = dict()
        for key, value in kwargs.items():
            if isinstance(value, dict):
                value = self.__class__(**value)
            else:
                value = interpolate(value)
            self.__store[key] = value

    def to_dict(self, secrets: Tuple[str, ...] = None) -> Dict:
        if not secrets:
            secrets = tuple()
        results = dict()
        for key, value in self.__store.items():
            if key in secrets:
                value = '************'
            elif isinstance(value, YamlConfig):
                value = value.to_dict(secrets=secrets)
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
        raise NotImplementedError

    def __delitem__(self, key: str) -> None:
        raise NotImplementedError

    def __getitem__(self, key: str) -> Any:
        return self.__store[key]

    def __len__(self) -> int:
        return len(self.__store)

    def __iter__(self) -> Iterator[str]:
        return iter(self.__store)

    def get(self, *keys: str, default: Any = None) -> Any:
        if len(keys) == 1:
            try:
                return self.__getitem__(keys[0])
            except KeyError:
                return default
        sub_store = self.__store[keys[0]]
        if not sub_store:
            raise KeyError(keys[0])
        return sub_store.get(*keys[1:], default=default)
