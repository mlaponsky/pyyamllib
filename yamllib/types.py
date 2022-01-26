from typing import Union, List, Optional

PrimitiveValue = Union[str, int, float, bool]
ConfigValue = Union[PrimitiveValue, List[PrimitiveValue]]


def cast_primitive(value: PrimitiveValue) -> PrimitiveValue:
    if not isinstance(value, str):
        return value
    value_lower = value.lower()
    if value_lower in ('true', 'false'):
        return value_lower == 'true'

    try:
        return int(value_lower)
    except ValueError:
        pass

    try:
        return float(value_lower)
    except ValueError:
        pass

    return value


def cast(value: ConfigValue) -> Optional[ConfigValue]:
    if not value:
        return None
    if ',' in value:
        value = value.split(',')
    if isinstance(value, list):
        return [cast_primitive(val) for val in value]
    return cast_primitive(value)
